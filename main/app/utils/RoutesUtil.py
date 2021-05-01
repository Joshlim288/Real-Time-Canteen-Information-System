import pprint
from datetime import datetime


class RoutesUtil():

    # TODO Change current_day_index default value
    @staticmethod
    def sort_operating_hours(restaurant_operating_hours, current_day_index=datetime(2019, 10, 10, 11, 0, 0, 0).isoweekday()):
        if restaurant_operating_hours is None or []:
            return []

        current_found = False
        before_current_day, after_current_day, sorted_list = [], [], []

        for index in restaurant_operating_hours:
            day_operating_hours = (index, restaurant_operating_hours[index])
            if index == current_day_index and current_found is False:
                sorted_list.append(day_operating_hours)
                current_found = True
            elif current_found is False:
                before_current_day.append(day_operating_hours)
            else:
                after_current_day.append(day_operating_hours)

            index += 1

        sorted_list.extend(after_current_day)
        sorted_list.extend(before_current_day)
        pprint.pprint(sorted_list)
        return sorted_list

    @staticmethod
    def assign_menu_items(menus):
        main_menu_items, drinks_menu_items, sides_menu_items = [], [], []
        for menu in menus:
            for menu_item in menu["menu_items"]:
                menu_item_category = menu_item["category"]
                if menu_item_category == 0:
                    main_menu_items.append(menu_item)
                elif menu_item_category == 1:
                    drinks_menu_items.append(menu_item)
                elif menu_item_category == 2:
                    sides_menu_items.append(menu_item)
        return [main_menu_items, drinks_menu_items, sides_menu_items]
