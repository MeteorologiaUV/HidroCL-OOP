# coding=utf-8

def get_catchment_name(catchment, catchment_names):
    """Get catchment name"""
    match catchment:
        case str():
            if catchment in catchment_names:
                return catchment
            else:
                print('Catchment not found')
                return
        case int():
            if catchment < len(catchment_names):
                return catchment_names[catchment]
            else:
                print('Catchment index out of range')
                return
        case _:
            print('Catchment not found')
            return
