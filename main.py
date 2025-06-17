import sys
import os

sys.stdout = open(os.devnull, 'w')
os.environ['KIVY_NO_CONSOLELOG'] = '1'

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.metrics import dp
from Foto_save import capture_photo, save_photo, permanent_photo_delete
from Foto_tags import add_tag, get_tags, search_tags, delete_tags
from plyer import filechooser
import re
import cv2
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout



class ClothingCatalogApp(MDApp):
    def build(self):
        
        
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.accent_palette = "Purple"
        self.theme_cls.theme_style = "Light"
        
        self.root = MDFloatLayout()
        
        self.clothing_items = [
            ['Backpack', ['A4', 'small', 'for laptop', 'extra size']],
            ['Blazer', ['casual', 'formal']],
            ['Blouse', ['short sleeve', 'long sleeve']],
            ['Coat', ['winter', 'transitional', 'leather', 'long', 'short']],
            ['Dresses', ['short', 'long', 'formal', 'summer']],
            ['Gloves', ['knitted', 'warm (winter)']],
            ['Handbag', ['A4', 'small', 'formal', 'extra size', 'fanny pack']],
            ['Hat', ['visor', 'winter', 'knitted']],
            ['Hoodies', ['with hood', 'without hood', 'short sleeve', 'long sleeve', 'button-up']],
            ['Jacket', ['winter', 'transitional', 'leather', 'long', 'short']],
            ['Pants', ['shorts', 'long', 'jeans', 'formal', 'baggy', 'tight', 'leggings', 'thermal', 'sporty']],
            ['Scarves', ['neck warmer', 'knitted']],
            ['Shoes', ['sandals', 'sneakers', 'heels', 'boots', 'high heels', 'flat', 'winter boots', 'crocs', 'ballet flats', 'dance shoes', 'laces', 'zip']],
            ['Skirts', ['short', 'long']],
            ['Sweater', ['short sleeve', 'long sleeve', 'button-up', 'cardigan', 'knitted', 'turtleneck', 'pullover']],
            ['T-shirts', ['short sleeve', 'long sleeve', 'tank top', 'thermal', 'compression', 'sporty']],
            ['Wigs', ['long', 'short', 'bob']]
        ]
        
        self.create_ui()
        return self.root
    
    def create_ui(self):
        # Background image
        self.background_image = Image(
            source=os.path.join(os.path.dirname(__file__), 'Backround_1.png'),
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.root.add_widget(self.background_image)
        
        # App title
        title = MDLabel(
            text="My Wardrobe",
            font_style="H4",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        self.root.add_widget(title)
        
        # Main menu card
        menu_card = MDCard(
            orientation="vertical",
            padding=dp(16),
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=4,
            radius=[20]
        )
        
        # Add item button
        add_item_btn = MDRaisedButton(
            text="Add a New Item",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.save_mod
        )
        menu_card.add_widget(add_item_btn)
        
        # Spacer
        menu_card.add_widget(MDBoxLayout(size_hint_y=None, height=dp(20)))
        
        # Explore items button
        explore_btn = MDRaisedButton(
            text="Explore Items",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            md_bg_color=self.theme_cls.accent_color,
            on_release=self.search_photos
        )
        menu_card.add_widget(explore_btn)
        
        # Spacer
        menu_card.add_widget(MDBoxLayout(size_hint_y=None, height=dp(20)))
        
        # Exit button
        exit_btn = MDFlatButton(
            text="Exit App",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            on_release=self.exit_app
        )
        menu_card.add_widget(exit_btn)
        
        self.root.add_widget(menu_card)
    
    def exit_app(self, instance):
        exit()
    
    def screen_reset(self):
        self.root.clear_widgets()
        self.root.add_widget(self.background_image)
    
    def back_to_main_menu(self, instance):
        self.screen_reset()
        self.create_ui()
    
    def save_mod(self, instance):
        self.screen_reset()
        
        # Create a card for the image capture section
        capture_card = MDCard(
            orientation="vertical",
            padding=dp(16),
            size_hint=(0.9, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=4,
            radius=[20]
        )
        
        # Title
        title = MDLabel(
            text="Add New Item",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(50)
        )
        capture_card.add_widget(title)
        
        # Image preview
        self.image = Image(
            size_hint=(1, 0.6)
        )
        capture_card.add_widget(self.image)
        
        # Buttons layout
        buttons_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(50),
            padding=[0, dp(20), 0, 0]
        )
        
        # Upload button
        upload_btn = MDRaisedButton(
            text="Upload Image",
            size_hint=(0.5, None),
            height=dp(50),
            on_release=self.open_filechooser
        )
        buttons_layout.add_widget(upload_btn)
        
        # Capture button
        capture_btn = MDRaisedButton(
            text="Take Photo",
            size_hint=(0.5, None),
            height=dp(50),
            on_release=self.capture_photo_action
        )
        buttons_layout.add_widget(capture_btn)
        
        capture_card.add_widget(buttons_layout)
        
        # Next button
        next_btn = MDRaisedButton(
            text="Next",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.save_photo_action
        )
        capture_card.add_widget(MDBoxLayout(size_hint_y=None, height=dp(20)))
        capture_card.add_widget(next_btn)
        
        # Back button
        back_btn = MDFlatButton(
            text="Back",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            on_release=self.back_to_main_menu
        )
        capture_card.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))
        capture_card.add_widget(back_btn)
        
        self.root.add_widget(capture_card)
        
        self.captured_frame = None
        self.current_photo_id = None
    

    def on_file_selected(self, selection):
        if selection:
            selected_file = selection[0]
            print(f"File selected: {selected_file}")
            
            # Read the selected image using OpenCV
            image = cv2.imread(selected_file)
            if image is None:
                print("Error: Unable to read the selected image.")
                return
            
            # Store the selected image in a variable
            self.selected_image = image

            # Display the selected image in the Image widget
            self.image.source = selected_file
            self.image.reload()
    

    
    def show_error_dialog(self, text):
        dialog = MDDialog(
            title="Error",
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    def search_photos(self, instance):
        self.screen_reset()
        
        # Clothing items
        self.search_clothing_item_names = [item[0] for item in self.clothing_items]
        self.search_clothing_item_dict = {item[0]: item[1] for item in self.clothing_items}
        
        # Create the first Spinner (dropdown box)
        self.search_main_spinner = Spinner(
            text='Select type',
            values=self.search_clothing_item_names,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        self.search_main_spinner.bind(text=self.update_search_sub_spinner_2)
        self.root.add_widget(self.search_main_spinner)

        # Create the second Spinner (dropdown box)
        self.search_dropdown = DropDown()

        # List to store selected items for search
        self.search_selected_items = []

        # Create a main button for search sub-items
        search_main_button = Button(text='Select Sub-types', size_hint=(0.5, None), height=44, pos_hint={'center_x': 0.5, 'center_y': 0.7})
        search_main_button.bind(on_release=self.search_dropdown.open)
        self.root.add_widget(search_main_button)

        # Input for search brand
        self.search_brand_input = TextInput(
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            hint_text='Type the Brand here'
        )
        self.root.add_widget(self.search_brand_input)

        # Input for search material
        self.search_material_input = TextInput(
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            hint_text='Type any other tags separated by commas (material, cost...)'
        )
        self.root.add_widget(self.search_material_input)

        # Button to save search tags
        self.search_save_tag_button = Button(
            text="Save Tags",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )

        # Color dropdown for search
        self.search_color_dropdown = DropDown()

        # List to store selected colors for search
        self.search_selected_colors = []

        # Create a main button for search colors
        self.search_color_main_button = Button(text='Select Colors', size_hint=(0.5, None), height=44, pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.search_color_main_button.bind(on_release=self.search_color_dropdown.open)
        # self.root.add_widget(self.search_color_main_button)

        # List of colors for search
        search_colors = sorted([
            "black", "red", "green", "blue", "yellow", "purple", "white", "pink",
            "mix of colors", "floral", "gold", "silver", "beige", "brown"
        ])
        
        for color in search_colors:
            btn = Button(text=f'{color}', size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_search_item(btn))
            self.search_color_dropdown.add_widget(btn)

        self.root.add_widget(self.search_color_main_button)

        self.search_photos_button = Button(
            text="Next",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.search_photos_button.bind(on_press=self.search_photos_action)
        self.root.add_widget(self.search_photos_button)
    def back_to_main_menu(self,instance):
        self.screen_reset()
        self.create_ui()
    def search_photos_action(self, instance):
        self.screen_reset()
        tags = []
        if self.search_main_spinner.text != "Select type":
             tags.append(self.search_main_spinner.text)
        tags.extend(self.search_selected_items)
        tags.append(self.search_brand_input.text)
        tags.append(self.search_material_input.text)
        tags.extend(self.search_selected_colors)
        
        print(tags)

        
        self.photos_with_the_tags = search_tags(tags) 
        print(self.photos_with_the_tags)
        if not self.photos_with_the_tags:
            self.show_error_dialog("No photos found with the selected tags.")
            return
        
        self.back_to_main_menu_button = MDRaisedButton(text = "Back",
                                        size_hint=(0.3, 0.15),
                                        size=(100, 100),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.1})
        self.back_to_main_menu_button.bind(on_press=self.back_to_main_menu)
        self.root.add_widget(self.back_to_main_menu_button)
        scroll_view = ScrollView(size_hint=(None, None), size=(500, 450), pos_hint={'center_x': 0.5, 'center_y': 0.6})

        # Create a GridLayout to hold images
        grid_layout = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Add images as buttons to the grid layout
        image_paths = [

        ]
        for photo_id in self.photos_with_the_tags:
            photo = f"photos/photo{photo_id}.png"
            image_paths.append(photo)
        for image_path in image_paths:
            # Create a Button with the image as background
            button = Button(
                background_normal=image_path,
                background_down=image_path,
                size_hint_y=None,
                height=250,
             

                on_press=self.on_image_press
            )
            grid_layout.add_widget(button)
        
        # Add the GridLayout inside the ScrollView
        scroll_view.add_widget(grid_layout)
        
        # Add the ScrollView to the root widget
        self.root.add_widget(scroll_view)
    def on_image_press(self, instance):
        # Action when an image button is pressed
        print(f"Image pressed: {instance.background_normal}")
        file_path = instance.background_normal

        # Extract the file name from the path
        file_name = os.path.basename(file_path)

        # Use regular expression to find numbers in the file name
        self.number = re.findall(r'\d+', file_name)

        # Extracted number (or "No number found" if no match)
        self.number_text = self.number[0] if self.number else "No number found"
        
        number_text_tags = get_tags(str(self.number_text))
        number_text_tags = ' - '.join(number_text_tags)

        self.show_popup(number_text_tags)
    def show_popup(self, number_text_tags):
        self.dialog = MDDialog(
            title="Photo Info",
            text=f"{number_text_tags}",
            buttons=[
            MDFlatButton(
                text="Close",
                theme_text_color="Custom",
                text_color=self.theme_cls.primary_color,
                on_release=self.dismiss_popup
            ),
            MDIconButton(
                icon="trash-can",
                theme_text_color="Custom",
                text_color=self.theme_cls.error_color,
                on_release=self.photo_remove
            ),
            ],
        )
        self.dialog.open()



    def photo_remove(self,instance):
        
        permanent_photo_delete(self.number_text)
        delete_tags(self.number_text)
        self.dismiss_popup(instance)
    def dismiss_popup(self, instance):
        # Close the popup when the dismiss button is pressed
        if self.dialog:
            self.dialog.dismiss()
        else:
            print("No popup found to dismiss.")
    def update_search_sub_spinner_2(self, spinner, text):
        self.search_sub_spinner = self.search_clothing_item_dict.get(text, [])
        # Clear the dropdown before adding new items
        self.search_dropdown.clear_widgets()
        
        # Add sub-items to the dropdown
        for index in self.search_sub_spinner:
            btn = Button(text=f'{index}', size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_search_item(btn))
            self.search_dropdown.add_widget(btn)
    def select_search_item(self, btn):
        if btn.text in self.search_selected_colors:
            self.search_selected_colors.remove(btn.text)
            btn.background_color = (1, 1, 1, 1)  # Reset to default color
        else:
            self.search_selected_colors.append(btn.text)
            btn.background_color = [218/255 * 2, 165/255 * 2, 32/255 * 2, 1]
    def screen_reset(self):
        self.root.clear_widgets()
       
        self.root.add_widget(self.background_image)

    def capture_photo_action(self, instance):
        frame = capture_photo()
        if frame is not None:
            self.captured_frame = frame
            # Convert the frame to a texture
            buf = frame.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            texture.flip_vertical()
            self.image.texture = texture
    def open_filechooser(self, instance):
        # Open the system's gallery to select an image
        filechooser.open_file(on_selection=self.on_file_selected, filters=['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif'])
    def on_file_selected(self, selection):
        # Check if something is selected from the file chooser
        if selection:
            selected_file = selection[0]
            print(f"File selected: {selected_file}")
            
            # Read the selected image using OpenCV
            image = cv2.imread(selected_file)
            if image is None:
                print("Error: Unable to read the selected image.")
                return
            
            # Store the selected image in a variable
            self.selected_image = image

            # Display the selected image in the Image widget
            self.image.source = selected_file
            self.image.reload()
    def save_photo_action(self, instance):
        if self.captured_frame is not None:
            # Save the captured frame
            photo_path, photo_id = save_photo(self.captured_frame)
        elif hasattr(self, 'selected_image') and self.selected_image is not None:
            # Save the selected image
            photo_path, photo_id = save_photo(self.selected_image)
        else:
            print("Error: No photo to save.")
            self.show_error_dialog("Please select or capture a photo.")
            return

        self.current_photo_id = photo_id
        self.image.source = photo_path
        self.image.reload()

        self.screen_reset()

        # Extract the names of the clothing items
        self.clothing_item_names = [item[0] for item in self.clothing_items]
        self.clothing_item_dict = {item[0]: item[1] for item in self.clothing_items}
        
        # Create the first Spinner (dropdown box)
        self.main_spinner = Spinner(
            text='Select type',
            values=self.clothing_item_names,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        self.main_spinner.bind(text=self.update_sub_spinner_1)
        self.root.add_widget(self.main_spinner)

        # Create the second Spinner (dropdown box)
        self.dropdown = DropDown()

        # List to store selected items
        self.selected_items = []

        # Create a main button
        main_button = Button(text='Select sub-types', size_hint=(0.5, None), height=44, pos_hint={'center_x': 0.5, 'center_y': 0.7})
        main_button.bind(on_release=self.dropdown.open)
        self.root.add_widget(main_button)

        self.brand_input = TextInput(
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            hint_text='Type the Brand here'
        )
        self.root.add_widget(self.brand_input)

        self.material_input = TextInput(
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            hint_text='Type any other tags separated by commas'
        )
        self.root.add_widget(self.material_input)

        self.color_dropdown = DropDown()

        # List to store selected items
        self.selected_colors = []

        # Add items to the dropdown
        colors = sorted([
            "black", "red", "green", "blue", "yellow", "purple", "white", "pink",
            "mix of colors", "floral", "gold", "silver", "beige", "brown"
        ])
        for color in colors:
            btn = Button(text=f'{color}', size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_color(btn))
            self.color_dropdown.add_widget(btn)

        self.color_main_button = Button(text='Select colors', size_hint=(0.5, None), height=44, pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.color_main_button.bind(on_release=self.color_dropdown.open)
        self.root.add_widget(self.color_main_button)

        self.save_tag_button = Button(
            text="Save item",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        self.save_tag_button.bind(on_press=self.save_tag_action)
        self.root.add_widget(self.save_tag_button)
    def save_tag_action(self, instance):
            
            
            tags = []
            tags.append(self.main_spinner.text)
            tags.extend(self.selected_items)
            tags.append(self.brand_input.text)
            tags.append(self.material_input.text)
            tags.extend(self.selected_colors)

            for tag in tags:
                photo_id = str(self.current_photo_id)  # Assuming current_photo_id is defined
                add_tag(photo_id, tag)
                print(f"Tag '{tag}' added to photo ID '{photo_id}'")
            self.screen_reset()
            self.create_ui()  
    def select_item(self, btn):
        if btn.text in self.selected_items:
            self.selected_items.remove(btn.text)
            btn.background_color = (1, 1, 1, 1)  # Reset to default color
        else:
            self.selected_items.append(btn.text)
            btn.background_color = [218/255 * 2, 165/255 * 2, 32/255 * 2, 1]
    def select_color(self, btn):
        if btn.text in self.selected_colors:
            self.selected_colors.remove(btn.text)
            btn.background_color = (1, 1, 1, 1)  # Reset to default color
        else:
            self.selected_colors.append(btn.text)
            btn.background_color = [218/255 * 2, 165/255 * 2, 32/255 * 2, 1]
    def update_sub_spinner_1(self, spinner, text):
        self.sub_spinner = self.clothing_item_dict.get(text, [])
        for index in self.sub_spinner:
                btn = Button(text=f'{index}', size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.select_item(btn))
                self.dropdown.add_widget(btn)

if __name__ == '__main__':
    ClothingCatalogApp().run()
