# Navbar content
def navbarItems(request):
    navbar_items = [
        {
            "url_name": "brewery",
            "icon_class": "bi-puzzle",
            "icon_width": 25,
            "icon_height": 25,
            "label": "Brewery",
            "aria_label": "Brewery"
        },
        {
            "url_name": "brewLog",
            "icon_class": "bi-journal-bookmark-fill",
            "icon_width": 20,
            "icon_height": 20,
            "label": "Brew Log",
            "aria_label": "Brew Log"
        },
        # {
        #     "url_name": "logout",
        #     "icon_class": "bi-box-arrow-right",
        #     "icon_width": 20,
        #     "icon_height": 20,
        #     "label": "Logout",
        #     "aria_label": "Logout"
        # }
    ]

    return {
        "navbar_items": navbar_items
    }
