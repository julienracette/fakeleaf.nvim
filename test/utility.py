def cookies_to_header(cookie_jar):
    key = ""
    for c in cookie_jar:
         key += f"{c.name}={c.value}; "
    return key
