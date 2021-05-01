from bson import ObjectId

"""
Data is curated such that all menus are available at:
2019-11-05T10:00:00Z
(Tuesday)
And they have the shortest waiting time of all restaurants
(Between 2-4)
"""

curated_restaurants = {
    "mcdonalds":    {
        "_id": ObjectId(),
        "name": "Mcdonalds",
        "information": "Sells hamburgers, various types of chicken, chicken sandwiches, \
                       French fries, soft drinks, breakfast items, and desserts.",
        "logo": "https://www.thesun.co.uk/wp-content/uploads/2017/02/nintchdbpict000177708607.jpg"
    },
    "subway":    {
        "_id": ObjectId(),
        "name": "Subway",
        "information": "Restaurant chain specializing in submarine sandwiches.",
        "logo": "https://cdn.iconscout.com/icon/free/png-256/subway-4-226366.png"
    },
    "kfc":    {
        "_id": ObjectId(),
        "name": "KFC",
        "information": "Fast food restaurant chain that specializes in fried chicken.",
        "logo": "http://media1.s-nbcnews.com/j/msnbc/Components/Photos/061113/061113_kfc_logo_vmed5p.grid-4x2.jpg"
    },
    "ljs":    {
        "_id": ObjectId(),
        "name": "Long John Silvers",
        "information": "Fast food restaurant chain that specializes in seafood.",
        "logo": "https://i.pinimg.com/originals/bc/91/56/bc9156ce42ee36fa53825ac6a3bec869.jpg"
    },
    "tsg":    {
        "_id": ObjectId(),
        "name": "The Sandwich Guys",
        "information": "Fresh not fried healthy alternative sandwiches, pasta and potatoes",
        "logo": "https://ucarecdn.com/67afc46b-d93b-45d9-b375-67bf75e3b9b9/"
    },
    "umisushi":    {
        "_id": ObjectId(),
        "name": "Umisushi",
        "information": "Serves a variety of Japanese food including sushi, bento, udon and salads",
        "logo": "https://www.waterwaypoint.com.sg/images/umisushi.jpg"
    }
}

curated_menus = {
    "mcdonalds_regular_menu" : {
        "_id": ObjectId(),
        "restaurant_id": curated_restaurants["mcdonalds"]["_id"],
        "name": "Standard menu",
        "description": "Items available all day",
        "start_datetime": "2019-01-01T00:00:00Z",
        "end_datetime": "2019-01-01T00:00:00Z",
        "day_of_week": [1, 2, 3, 4, 5, 6, 7],
        "weekly_recurring": True,
        "menu_type": 0,
        "average_waiting_time": 3.52
    },
    "mcdonalds_morning_menu": {
        "_id": ObjectId(),
        "restaurant_id": curated_restaurants["mcdonalds"]["_id"],
        "name": "Breakfast menu",
        "description": "Morning only specials",
        "start_datetime": "2019-01-01T08:00:00Z",
        "end_datetime": "2019-01-01T11:00:00Z",
        "day_of_week": [1, 2, 3, 4, 5, 6, 7],
        "weekly_recurring": True,
        "menu_type": 0,
        "average_waiting_time": 2.62
    },
    "subway_regular_menu": {
        "_id": ObjectId(),
        "restaurant_id": curated_restaurants["subway"]["_id"],
        "name": "Standard menu",
        "description": "Eat fresh",
        "start_datetime": "2019-01-01T08:00:00Z",
        "end_datetime": "2019-01-01T20:00:00Z",
        "day_of_week": [1, 2, 3, 4, 5, 6, 7],
        "weekly_recurring": True,
        "menu_type": 0,
        "average_waiting_time": 4.12
    },
    "kfc_regular_menu": {
        "_id": ObjectId(),
        "restaurant_id": curated_restaurants["kfc"]["_id"],
        "name": "Standard menu",
        "description": "Finger lickin' good!",
        "start_datetime": "2019-01-01T08:00:00Z",
        "end_datetime": "2019-01-01T20:00:00Z",
        "day_of_week": [1, 2, 3, 4, 5, 6, 7],
        "weekly_recurring": True,
        "menu_type": 0,
        "average_waiting_time": 3.15
    },
    "kfc_promo_menu": {
        "_id": ObjectId(),
        "restaurant_id": curated_restaurants["kfc"]["_id"],
        "name": "6 for 9 special",
        "description": "6 pieces of chicken for $9, limited time only!",
        "start_datetime": "2019-11-01T08:00:00Z",
        "end_datetime": "2019-12-10T20:00:00Z",
        "day_of_week": [2],
        "weekly_recurring": False,
        "menu_type": 2,
        "average_waiting_time": 3.67
    },
    "ljs_regular_menu": {
        "_id": ObjectId(),
        "restaurant_id": curated_restaurants["ljs"]["_id"],
        "name": "Standard menu",
        "description": "We speak fish",
        "start_datetime": "2019-01-01T09:00:00Z",
        "end_datetime": "2019-01-01T19:00:00Z",
        "day_of_week": [1, 2, 3, 4, 5, 6, 7],
        "weekly_recurring": True,
        "menu_type": 0,
        "average_waiting_time": 1.97
    },
    "tsg_regular_menu": {
        "_id": ObjectId(),
        "restaurant_id": curated_restaurants["tsg"]["_id"],
        "name": "Standard menu",
        "description": "Fresh not fried",
        "start_datetime": "2019-01-01T08:00:00Z",
        "end_datetime": "2019-01-01T20:00:00Z",
        "day_of_week": [1, 2, 3, 4, 5],
        "weekly_recurring": True,
        "menu_type": 0,
        "average_waiting_time": 2.21
    },
    "umisushi_regular_menu": {
        "_id": ObjectId(),
        "restaurant_id": curated_restaurants["umisushi"]["_id"],
        "name": "Standard menu",
        "description": "Best sushi around!",
        "start_datetime": "2019-01-01T07:00:00Z",
        "end_datetime": "2019-01-01T17:00:00Z",
        "day_of_week": [1, 2],
        "weekly_recurring": True,
        "menu_type": 0,
        "average_waiting_time": 3.46
    }
}

curated_menu_items = {
    "kfc_regular_menu_items": [
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["kfc_regular_menu"]["_id"],
            "name": "Original Recipe Chicken",
            "price": 3.55,
            "image": "https://www.kfc.com.sg//Content/OnlineOrderingImages/Menu/Items/Chicken_OriginalRcipe_1.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["kfc_regular_menu"]["_id"],
            "name": "Hot & Crispy Chicken",
            "price": 3.55,
            "image": "https://www.kfc.com.sg//Content/OnlineOrderingImages/Menu/Items/Chicken_Hot&Crispy_1.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["kfc_regular_menu"]["_id"],
            "name": "Zinger Burger",
            "price": 5.30,
            "image": "https://www.kfc.com.sg//Content/OnlineOrderingImages/Menu/Items/BurgerWraps_Zinger_1.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["kfc_regular_menu"]["_id"],
            "name": "Hot & Crispy Tenders",
            "price": 6.80,
            "image": "https://www.kfc.com.sg//Content/OnlineOrderingImages/Menu/Items/Sides_H&CTenders5pcs_2.jpg",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["kfc_regular_menu"]["_id"],
            "name": "Nuggets (6 pcs)",
            "price": 4.30,
            "image": "https://www.kfc.com.sg//Content/OnlineOrderingImages/Menu/Items/Sides_Nuggets6pcs_New_1.jpg",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["kfc_regular_menu"]["_id"],
            "name": "Pepsi (reg)",
            "price": 2.80,
            "image": "https://www.kfc.com.sg//Content/OnlineOrderingImages/Menu/Items/Drinks_PepsiReg_1.jpg",
            "category": 2
        }
    ],
    "kfc_special_menu_items":  [
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["kfc_promo_menu"]["_id"],
            "name": "Mac N Cheese O.R Burger",
            "price": 6.70,
            "image": "https://www.kfc.com.sg//Content/OnlineOrderingImages/Menu/Items/DEL_MAC_OR_Burger.jpg",
            "category": 0
        }
    ],
    "mcdonalds_regular_menu_items": [
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_regular_menu"]["_id"],
            "name": "Cheeseburger",
            "price": 2.50,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04043431/product-cheeseburger-350x350.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_regular_menu"]["_id"],
            "name": "Double Cheeseburger",
            "price": 3.50,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04043525/product-double-cheeseburger-350x350.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_regular_menu"]["_id"],
            "name": "McSpicy",
            "price": 3.50,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04044056/product-mcspicy-350x350.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_regular_menu"]["_id"],
            "name": "French Fries (S)",
            "price": 1.50,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04044451/product-french-fries-350x350.png",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_regular_menu"]["_id"],
            "name": "Corn Cup",
            "price": 1.00,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04034257/product-corn-350x350.png",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_regular_menu"]["_id"],
            "name": "Coca-Cola",
            "price": 1.50,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04115241/Bell-Soda-Glass-Less-SG-350x350.png",
            "category": 2
        }
    ],
    "mcdonalds_morning_menu_items": [
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_morning_menu"]["_id"],
            "name": "Egg McMuffin",
            "price": 2.00,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04032446/product-egg-mcmuffin-350x350.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_morning_menu"]["_id"],
            "name": "Sausage McMuffin",
            "price": 3.00,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04033140/product-sausage-mcmuffin-w-egg-350x350.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_morning_menu"]["_id"],
            "name": "Big Breakfast",
            "price": 4.00,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04031748/product-big-breakfast-350x350.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_morning_menu"]["_id"],
            "name": "Hashbrown",
            "price": 1.00,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04034143/product-hashbrown-single-350x350.png",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["mcdonalds_morning_menu"]["_id"],
            "name": "Iced Milo",
            "price": 1.50,
            "image": "https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/04/04035956/product-milo-350x350.png",
            "category": 2
        }
    ],
    "Subway_regular_menu_items": [
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["subway_regular_menu"]["_id"],
            "name": "Chicken & Bacon Ranch Melt",
            "price": 5.00,
            "image": "https://www.subway.com/ns/images/menu/CAN/ENG/ChickenBaconRanchRotisserie_6-Inch_234X140_72_RGB.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["subway_regular_menu"]["_id"],
            "name": "Steak & Cheese",
            "price": 7.00,
            "image": "https://www.subway.com/ns/images/menu/CAN/ENG/menu-category-sandwich-SteakCheese-234x140.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["subway_regular_menu"]["_id"],
            "name": "Italian B.M.T",
            "price": 5.00,
            "image": "https://www.subway.com/ns/images/menu/CAN/ENG/menu-category-sandwich-ItalianBMT-234x140.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["subway_regular_menu"]["_id"],
            "name": "Cookies",
            "price": 2.00,
            "image": "https://www.subway.com/ns/images/menu/CAN/ENG/Subway_CaramelAppleCookie_234x140_72_RGB.jpg",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["subway_regular_menu"]["_id"],
            "name": "Chips",
            "price": 2.00,
            "image": "https://www.subway.com/ns/images/menu/CAN/ENG/Subway_SunChipsGarden_234x140_72_RGB.jpg",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["subway_regular_menu"]["_id"],
            "name": "Soft Drink",
            "price": 1.50,
            "image": "https://www.subway.com/ns/images/menu/CAN/ENG/Subway_12-oz_CoffeeCup_234x140_72_RGB.jpg",
            "category": 2
        }
    ],
    "ljs_regular_menu_items": [
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["ljs_regular_menu"]["_id"],
            "name": "1pc Fish with Crispy Fries and Coca-Cola/Sprite (R)",
            "price": 5.00,
            "image": "https://www.longjohnsilvers.com.sg/assets/img/menu-gv-1pc-fish.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["ljs_regular_menu"]["_id"],
            "name": "2pc Chicken with Crispy Fries and Coca-Cola/Sprite (R)",
            "price": 5.00,
            "image": "https://www.longjohnsilvers.com.sg/assets/img/menu-gv-2pc-fish.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["ljs_regular_menu"]["_id"],
            "name": "Chilli Crab Fish Rice Bowl with Coca-Cola/Sprite (R)",
            "price": 5.50,
            "image": "https://www.longjohnsilvers.com.sg/assets/img/menu-chillicrab-rice.png",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["ljs_regular_menu"]["_id"],
            "name": "Coleslaw",
            "price": 1.90,
            "image": "https://www.longjohnsilvers.com.sg/assets/img/menu-ccf-coleslaw-2.png",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["ljs_regular_menu"]["_id"],
            "name": "Crispy Fries",
            "price": 2.50,
            "image": "https://www.longjohnsilvers.com.sg/assets/img/menu-ccf-crispy-fries-2.png",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["ljs_regular_menu"]["_id"],
            "name": "Ice Lemon Tea",
            "price": 2.80,
            "image": "https://www.longjohnsilvers.com.sg/assets/img/menu-c-ice-lemon-tea-new.png",
            "category": 2
        }
    ],
    "tsg_regular_menu_items": [
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["tsg_regular_menu"]["_id"],
            "name": "BBQ Pulled Pork Sandwich",
            "price": 4.00,
            "image": "https://burpple-2.imgix.net/foods/3b8459642ed0d9014161404245_original.?w=350&dpr=1&fit=crop&q=80&auto=format",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["tsg_regular_menu"]["_id"],
            "name": "Cajun Grilled Chicken Sandwich",
            "price": 4.00,
            "image": "https://burpple-2.imgix.net/foods/3e9eda3e5fb9fe679fa1390545_original.?w=350&dpr=1&fit=crop&q=80&auto=format",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["tsg_regular_menu"]["_id"],
            "name": "Ice Lemon Tea",
            "price": 2.80,
            "image": "https://www.longjohnsilvers.com.sg/assets/img/menu-c-ice-lemon-tea-new.png",
            "category": 2
        }
    ],
    "umisushi_regular_menu_items": [
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["umisushi_regular_menu"]["_id"],
            "name": "Gyu Don",
            "price": 8.70,
            "image": "https://order.umisushi.com.sg/img/menus/v2/3_Donburi/Gyu%20Don.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["umisushi_regular_menu"]["_id"],
            "name": "Assorted Salmon Sushi",
            "price": 12.50,
            "image": "https://order.umisushi.com.sg/img/menus/v2/6_Mini%20Platters/All%20Salmon.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["umisushi_regular_menu"]["_id"],
            "name": "Sushi & Maki",
            "price": 7.30,
            "image": "https://order.umisushi.com.sg/img/menus/v2/6_Mini%20Platters/Sushi%20and%20Maki.jpg",
            "category": 0
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["umisushi_regular_menu"]["_id"],
            "name": "Chuka Idako",
            "price": 2.90,
            "image": "https://order.umisushi.com.sg/img/menus/v2/10_Appetisers/Chuka%20Idako.jpg",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["umisushi_regular_menu"]["_id"],
            "name": "Chuka Kurage",
            "price": 2.90,
            "image": "https://order.umisushi.com.sg/img/menus/v2/10_Appetisers/Chuka%20Kurage.jpg",
            "category": 1
        },
        {
            "_id": ObjectId(),
            "menu_id": curated_menus["umisushi_regular_menu"]["_id"],
            "name": "Sprite",
            "price": 1.90,
            "image": "https://order.umisushi.com.sg/img/menus/v2/12_Drinks/Sprite.jpg",
            "category": 2
        }
    ]
}
