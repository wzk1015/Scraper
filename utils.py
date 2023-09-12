def text_contains(tag, substr, tag_name=None):   
    if tag_name is not None and tag.name != tag_name:
        return False
    return substr in tag.text


def class_starts_with(tag, prefix, tag_name=None): 
    if tag_name is not None and tag.name != tag_name:
        return False
    if not tag.has_attr('class'):
        return False
    return tag["class"][0].startswith(prefix)

def class_contains(tag, substr, tag_name=None): 
    if tag_name is not None and tag.name != tag_name:
        return False
    if not tag.has_attr('class'):
        return False
    return substr in tag["class"]