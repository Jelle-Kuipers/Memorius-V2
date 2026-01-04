# Converts snake_case to Normal Case

def snake_to_normal(snake_str):
    components = snake_str.split('_')
    normal_str = ' '.join(x.title() for x in components)
    return normal_str