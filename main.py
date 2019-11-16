# -*- coding: utf-8 -*-
# encoding=utf-8

# https://github.com/kivy/kivy/blob/297dd024ce407f85d1210dac1730e2817a03606f/kivy/modules/screen.py
import traceback

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.modules import screen
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.managerswiper import MDSwiperPagination

from baseclass.box_bottom_sheet import PreviousImage
from baseclass.product_gallery import ProductsBox
from baseclass.product_screen import ProductScreen
from baseclass.shrine_root_screen import split_list

# screen.apply_device("phone_iphone_6", 0.50, "portrait")

was_here = False

Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import Window kivy.core.window.Window
#:import IconLeftWidget kivymd.uix.list.IconLeftWidget

#:import colors kivymd.color_definitions.colors
#:import gch kivy.utils.get_color_from_hex
#:import Clock kivy.clock.Clock
#:import environ os.environ


#:include kv/overview.kv
#:include kv/showcatalogue.kv
#:include kv/box_bottom_sheet.kv

#:include kv/product_screen.kv
#:include kv/product_gallery.kv

#:include backdrop_kv/overview_backdrop.kv

""")


class ShowCatalogueScreen(Screen):

    def __init__(self, **kwargs):
        super(ShowCatalogueScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        # determine kind of products to show
        if DigiComo().catalogue_category == "Mobile Phones":
            self.isMobilePhones()

    def isMobilePhones(self):
        products_list, products_description = self.set_products_list()
        self.add_products_box_to_image_list(products_list, products_description)

    def set_products_list(self):
        products_list = []
        products_description = [
            [
                "[b]iPhone 4[/b]\nN$1,120",
                "[b]iPhone 5[/b]\nN$1,190",
                "[b]iPhone 6[/b]\nN$1,200",
            ],
            [
                "[b]iPhone 6 Plus[/b]\nN$1,388",
                "[b]Samsung J5[/b]\nN$1,500",
                "[b]Note 8[/b]\nN$2,000",
            ],
            [
                "[b]Galaxy Fold[/b]\nN$2,399",
                "[b]Huawei P9 Lite[/b]\nN$2,000",
                "[b]Xiaomi Mi 9[/b]\nN$2,199",
            ],
            [
                "[b]Pixel 2[/b]\nN$2,499",
                "[b]Pixel 3[/b]\nN$2,899",
                "[b]Pixel 4[/b]\nN$2,999",
            ],
        ]

        for name_image in range(len(products_description)*3):
            products_list.append("phone.jpg")
        products_list = split_list(products_list, 3)

        return products_list, products_description

    def add_products_box_to_image_list(
        self, products_list, products_description
    ):
        for i, paths_to_images in enumerate(products_list):
            self.ids.product_gallery.add_widget(
                ProductsBox(
                    paths_to_images=paths_to_images,
                    products_description=products_description[i],
                    box_width=self.ids.image_list.width,
                    box_height=self.ids.image_list.height,
                    callback=self.add_product_to_box_bottom_sheet,
                    _root=self,
                )
            )

    def add_product_to_box_bottom_sheet(self, instanse_box_mage):
        self.ids.box_bottom_sheet.ids.previous_box.add_widget(
            PreviousImage(
                source=instanse_box_mage.ids.image_product.source,
                size_hint=(None, None),
                size=(dp(42), dp(42)),
                description=instanse_box_mage.ids.description.text,
                _root=self,
            )
        )
        self.ids.box_bottom_sheet.width + dp(52)
        width = self.ids.box_bottom_sheet.width + dp(52)
        Animation.stop_all(self)
        Animation(width=width, d=0.1).start(self.ids.box_bottom_sheet)

    def on_back_pressed(self):
        DigiComo().manage_screens(self.name, "remove")
        DigiComo().change_screen("overview_screen")


class OverviewScreen(Screen):

    def __init__(self, **kwargs):
        super(OverviewScreen, self).__init__(**kwargs)


class ItemBackdropBackLayer(ThemableBehavior, BoxLayout):
    icon = StringProperty("android")
    text = StringProperty()
    selected_item = BooleanProperty(False)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            for item in self.parent.children:
                if item.selected_item:
                    item.selected_item = False
            self.selected_item = True
            if self.text == "Mobile Phones":
                DigiComo.catalogue_category = "Mobile Phones"
                DigiComo().manage_screens("show_catalogue_screen", "add")
                DigiComo().change_screen("show_catalogue_screen")
        return super().on_touch_down(touch)


class FeaturedItemViewManager(BoxLayout):
    def __init__(self, **kwargs):
        super(FeaturedItemViewManager, self).__init__(**kwargs)
        # call on next frame as is still to load the ids
        Clock.schedule_once(self.setup, 0)

    def setup(self, dt):
        global was_here
        if was_here:
            # else we'll keep adding to the paginator
            return
        was_here = True
        s1 = Screen(name="s1")
        s1.add_widget(MyCard(text="iPhone 6 (16GB Memory) | N$2,860",
                             src="https://dqzrr9k4bjpzk.cloudfront.net/images/17745377/1123436338.jpg"))
        s2 = Screen(name="s2")
        s2.add_widget(MyCard(text="Orange Gqomington T-shirt | N$180",
                             src="https://dqzrr9k4bjpzk.cloudfront.net/images/17745377/1137407518.jpg"))
        s3 = Screen(name="s3")
        s3.add_widget(MyCard(text="iPhone 6 Plus (64GB Memory) | N$4,070",
                             src="https://dqzrr9k4bjpzk.cloudfront.net/images/17745377/1126169241.jpg"))

        self.ids.swiper_manager.add_widget(s1)
        self.ids.swiper_manager.add_widget(s2)
        self.ids.swiper_manager.add_widget(s3)


class MyCard(MDCard):
    text = StringProperty('')
    src = StringProperty('')
    extra_info = {}


class DigiComo(MDApp):
    global sm
    sm = ScreenManager()
    catalogue_category = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "DeepPurple"

    # dynamically add/remove screens to consume less memory

    def change_screen(self, screen_name):
        if sm.has_screen(screen_name):
            sm.current = screen_name
        else:
            print("Screen [" + screen_name + "] does not exist.")

    def manage_screens(self, screen_name, action):
        scns = {
            "overview_screen": OverviewScreen,
            "show_catalogue_screen": ShowCatalogueScreen,
            "product screen": ProductScreen
        }
        try:

            if action == "remove":
                if sm.has_screen(screen_name):
                    sm.remove_widget(sm.get_screen(screen_name))
                # print("Screen ["+screen_name+"] removed")
            elif action == "add":
                if sm.has_screen(screen_name):
                    print("Screen [" + screen_name + "] already exists")
                else:
                    sm.add_widget(scns[screen_name](name=screen_name))
                    print(screen_name + " added")
                    # print("Screen ["+screen_name+"] added")
        except:
            print(traceback.format_exc())

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        global sm
        self.bind(on_start=self.post_build_init)
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(OverviewScreen(name="overview_screen"))
        start_screen = FeaturedItemViewManager()
        self.swiper_manager = start_screen.ids.swiper_manager
        paginator = MDSwiperPagination()
        paginator.screens = self.swiper_manager.screen_names
        paginator.manager = self.swiper_manager
        self.swiper_manager.paginator = paginator
        start_screen.add_widget(paginator)
        from kivy.modules import inspector
        inspector.create_inspector(Window, sm)
        return sm

    def post_build_init(self, ev):
        win = self._app_window
        win.bind(on_keyboard=self._key_handler)

    def _key_handler(self, *args):
        key = args[1]
        # 1000 is "back" on Android
        # 27 is "escape" on computers
        if key in (1000, 27):
            try:
                sm.current_screen.dispatch("on_back_pressed")
            except Exception as e:
                print(e)
            return True
        elif key == 1001:
            try:
                sm.current_screen.dispatch("on_menu_pressed")
            except Exception as e:
                print(e)
            return True


if __name__ == "__main__":
    DigiComo().run()
