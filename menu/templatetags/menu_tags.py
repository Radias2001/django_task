from django import template
from menu.models import MenuItem, Menu

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    current_url = request.path if request else ''

    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_items': []}

    items = MenuItem.objects.filter(menu=menu).select_related('parent')

    item_map = {
        item.id: {
            'item': item,
            'children': [],
            'is_active': False,
            'is_open': False,
        } for item in items
    }

    root_items = []
    for item in items:
        node = item_map[item.id]
        if item.parent_id and item.parent_id in item_map:
            item_map[item.parent_id]['children'].append(node)
        else:
            root_items.append(node)

    for node in item_map.values():
        if node['item'].get_url() == current_url:
            node['is_active'] = True
            parent = node['item'].parent
            while parent and parent.id in item_map:
                item_map[parent.id]['is_open'] = True
                parent = parent.parent

    return {'menu_items': root_items}
