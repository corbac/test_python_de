def default_cleaner(data_frame):
    import pandas as pds

    def remove_notascii(x):
        import re
        try:
            # print(x)
            # print(re.sub(r'\\[a-z1-9]{3}',r'', x) )
            # print('*' * 99)
            return re.sub(r'\\[a-z1-9]{3}',r'', x) 
        except:
            return x

    data_frame = data_frame.drop_duplicates()
    data_frame = data_frame.applymap(remove_notascii)

    return data_frame

def reject_tag(item):
    import math
    import pandas

    # print(item)
    # print(type(item))
    # print(isinstance(item, float) )
    # print('------')
    if isinstance(item, float) and math.isnan(item):
        return True
    elif pandas.isnull(item):
        return True
    elif not item or (isinstance(item,str) and item.replace(' ', '') == ''):
        return True
    else:
        return False

def transform_date(item):
    from datetime import datetime
    # print(item)
    if isinstance(item, datetime):
        return item
    else:
        try:
            # assess format date as dd/mm/yy
            return datetime.strptime(item, '%d/%m/%y')
        except ValueError:
            try:
                # assess format date as dd/mm/yyyy
                return datetime.strptime(item, '%d/%m/%Y')
            except ValueError:
                try:
                    # assess US format date as mm/dd/yyyy
                    return datetime.strptime(item, '%d/%m/%Y')
                except ValueError:
                    try:
                        # assess format date as dd month yyyy
                        return datetime.strptime(item, '%d %B %Y') 
                    except ValueError:
                        try:
                            # assess US format date as dd mon yyyy
                            return datetime.strptime(item, '%d %b %Y') 
                        except ValueError:
                            # raise Exception("It Seems the date is not well formated")
                            return None

def json_cleaner(json_file_str):
    import re
    import os

    json_file_str = re.sub(r'\}\,[\n\r\t]*\]', '}%s]' % os.linesep, json_file_str)
    #Add another rules
    ...
    
    # print(json_file_str)
    return json_file_str
