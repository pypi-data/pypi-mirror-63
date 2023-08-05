'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import re
from enum import Enum, auto
from collections import namedtuple

from arjuna.core.enums import GuiElementType

class ImplWith:
    
    def __init__(self, *, wtype, wvalue, named_args, has_content_locator):
        self.wtype = wtype
        self.wvalue = wvalue
        self.named_args = named_args
        self.has_content_locator = has_content_locator

    def __str__(self):
        return "ImplWith: {}".format(vars(self))

class GenericLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    SELECTOR = auto()
    CLASSES = auto() 
    LINK = auto() 
    FLINK = auto()
    PLINK = auto() 
    TAG = auto()

    INDEX = auto()
    WINDOW_TITLE = auto()
    WINDOW_PTITLE = auto()
    ELEMENT = auto()
    POINT = auto()
    JS = auto() 

    # Translated to XPath
    TEXT = auto() 
    FTEXT = auto() 
    TITLE = auto() 
    TYPE = auto() 
    VALUE = auto() 
    ATTR = auto()
    FATTR = auto()
    IMAGE_SRC = auto()
    IMAGE = auto()

    # Translated 1-1 to Selenium
    PARTIAL_LINK_TEXT = auto()
    LINK_TEXT = auto()
    TAG_NAME = auto()
    CSS_SELECTOR = auto()

class Locator:

    def __init__(self, ltype, lvalue, named_args):
        self.ltype = ltype
        self.lvalue = lvalue
        self.__named_args = named_args

    def set_args(self,  named_args):
        self.__named_args = named_args

    @property
    def named_args(self):
        return self.__named_args

    def __str__(self):
        return str(vars(self))

    def is_layered_locator(self):
        return False

class GuiGenericLocator(Locator):

    def __init__(self, ltype, lvalue, named_args):
        super().__init__(ltype, lvalue, named_args)
    
    def set_value(self, value):
        self.lvalue = value

    def as_map(self):
        map = dict()
        map["withType"] = self.ltype.name
        if self.ltype.name.lower() != "content_locator":
            map["withValue"] = self.lvalue
        else:
            map["withValue"] = [l.as_map() for l in self.lvalue.locators]

        # if self.__named_args:
        #     map["named_args"] = self.__named_args
        
        return map

# class GuiGenericChildLocator(Locator):
#     def __init__(self, ltype, lvalue, named_args):
#         super().__init__(ltype, lvalue, named_args)
    
#     def set_value(self, value):
#         self.lvalue = value    

#     def is_layered_locator(self):
#         return True

from arjuna.core.adv.types import CIStringDict

class Meta:

    def __init__(self, mdict=None):
        self.__mdict = not mdict and CIStringDict() or CIStringDict(mdict)
        from arjuna.core.enums import GuiTemplate
        if "template" in self.__mdict:
            try:
                template = self.__mdict["template"]
                self.__template = GuiTemplate[template.upper()]
            except:
                raise Exception("{} is not a valid template type.".format(template))
        else:
            self.__template = GuiTemplate.ELEMENT

    @property
    def template(self):
        return self.__template

    def __str__(self):
        return str(self.__mdict)

class GuiElementMetaData:
    XPATH_TWO_ARG_VALUE_PATTERN = r'^\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]$'

    BASIC_LOCATORS = {
        GenericLocateWith.ID,
        GenericLocateWith.NAME,
        GenericLocateWith.XPATH,
        GenericLocateWith.IMAGE,
        GenericLocateWith.INDEX,
        GenericLocateWith.WINDOW_TITLE,
        GenericLocateWith.WINDOW_PTITLE,
        GenericLocateWith.POINT,
        GenericLocateWith.JS,
    }

    NEED_TRANSLATION = {
        GenericLocateWith.TAG : GenericLocateWith.TAG_NAME,
        GenericLocateWith.LINK : GenericLocateWith.PARTIAL_LINK_TEXT,
        GenericLocateWith.FLINK : GenericLocateWith.LINK_TEXT,
        GenericLocateWith.SELECTOR : GenericLocateWith.CSS_SELECTOR,
    }

    XTYPE_LOCATORS = {
        GuiElementType.TEXTBOX: "//input[@type='text']",
        GuiElementType.PASSWORD: "//input[@type='password']",
        GuiElementType.LINK: "//a",
        GuiElementType.BUTTON: "//input[@type='button']",
        GuiElementType.SUBMIT_BUTTON: "//input[@type='submit']",
        GuiElementType.DROPDOWN: "//select",
        GuiElementType.CHECKBOX: "//input[@type='checkbox']",
        GuiElementType.RADIO: "//input[@type='radio']",
        GuiElementType.IMAGE: "//img",
    }

    XPATH_LOCATORS = {
        GenericLocateWith.TEXT : "//*[contains(text(),'{}')]",
        GenericLocateWith.FTEXT : "//*[text()='{}']",
        GenericLocateWith.VALUE : "//*[@value='{}']",
        GenericLocateWith.TITLE : "//*[@title='{}']",
        GenericLocateWith.IMAGE_SRC : "//img[@src='{}']"
    }

    XPATH_TWO_ARG_LOCATORS = {
        GenericLocateWith.ATTR : "//*[contains(@{},'{}')]",
        GenericLocateWith.FATTR : "//*[@{}='{}']",
    }

    def __init__(self, raw_locators, meta=None, process_args=True):
        self.__raw_locators = raw_locators
        self.__locators = []
        self.__process()
        if process_args:
            self.process_args()
        self.__meta = Meta(meta)

    @property
    def meta(self):
        return self.__meta

    def __str__(self):
        return str([str(l) for l in self.__locators])

    def print_locators(self):
        print(str(self))

    @property
    def locators(self):
        return self.__locators

    @property
    def raw_locators(self):
        return self.__raw_locators

    def __process(self):
        for raw_locator in self.__raw_locators:
            rltype = raw_locator.ltype
            rlvalue = raw_locator.lvalue
            named_args = raw_locator.named_args
            try:
                generic_locate_with = GenericLocateWith[rltype.upper()]
            except:
                raise Exception("Invalid locator across all automators: {}={}".format(rltype, type(rlvalue)))
            else:
                if generic_locate_with == GenericLocateWith.ELEMENT:
                    self.__add_locator(generic_locate_with, rlvalue, named_args)
                elif generic_locate_with in self.BASIC_LOCATORS:
                    self.__add_locator(generic_locate_with, rlvalue, named_args)
                elif generic_locate_with in self.NEED_TRANSLATION:
                    self.__add_locator(self.NEED_TRANSLATION[generic_locate_with], rlvalue, named_args)
                elif generic_locate_with in self.XPATH_LOCATORS:
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_LOCATORS[generic_locate_with].format(rlvalue), named_args)
                elif generic_locate_with in self.XPATH_TWO_ARG_LOCATORS:
                    # parts = None
                    try:
                        rlvalue["name"]
                        rlvalue["value"]
                        #parts =  re.search(GuiElementMetaData.XPATH_TWO_ARG_VALUE_PATTERN, rlvalue).groups()
                    except:
                        raise Exception("Value {} for {} is misformatted. Attribute name and attribute value should be supplied as: [<arg>][<value>]".format(rlvalue, rltype))
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_TWO_ARG_LOCATORS[generic_locate_with].format(rlvalue["name"], rlvalue["value"]), named_args)
                elif generic_locate_with == GenericLocateWith.TYPE:
                    try:
                        elem_type = GuiElementType[rlvalue.upper()]
                    except:
                        raise Exception("Unsupported element type for XTYPE locator: " + rlvalue)
                    else:
                        self.__add_locator(GenericLocateWith.XPATH, self.XTYPE_LOCATORS[elem_type], named_args)
                # elif generic_locate_with == GenericLocateWith.COMPOUND_CLASS:
                #     self.__add_locator(GenericLocateWith.CSS_SELECTOR, re.sub(r'\s+', '.', ), named_args)
                elif generic_locate_with == GenericLocateWith.CLASSES:
                    css_string = None
                    if type(rlvalue) is str:
                        css_string = "." + rlvalue.replace('.', ' ').strip()
                    else:
                        if type(rlvalue[0]) is str:
                            css_string = "." + rlvalue[0].replace('.', ' ').strip()
                        else:
                            css_string = "." + ".".join(rlvalue[0])
                    self.__add_locator(GenericLocateWith.CSS_SELECTOR, re.sub(r'\s+', '.', css_string), named_args)
                else:
                    raise Exception("Locator not supported yet by Arjuna: " + rltype)

    def __add_locator(self, locator_type, locator_value, named_args):
        self.locators.append(GuiGenericLocator(locator_type, locator_value, named_args))

    def process_args(self):
        '''
            It consumes impl locator list.
        '''
        pattern = r"\$(\s*\w*?\s*)\$"
        for locator in self.locators:
            if locator.ltype == GenericLocateWith.ELEMENT:
                locator.lvalue.process_args()

            if not locator.named_args: continue

            fmt_locator_value = locator.lvalue.replace("\{", "__LB__").replace("}", "__RB__")

            # Find params
            matches = re.findall(pattern, fmt_locator_value)
            
            for match in matches:
                target = "${}$".format(match)
                repl = "{" + match.lower().strip() + "}"
                fmt_locator_value = fmt_locator_value.replace(target, repl)

            repl = {k.lower():v for k,v in locator.named_args.items()}
            fmt_locator_value = fmt_locator_value.format(**repl)
            fmt_locator_value = fmt_locator_value.replace("__LB__", "{").replace("__RB__", "}")
            locator.set_value(fmt_locator_value)


    @classmethod
    def __process_single_raw_locator(cls, impl_locator):
        ltype = impl_locator.wtype
        lvalue = impl_locator.wvalue
        p_locator = Locator(ltype=ltype, lvalue=lvalue, named_args=impl_locator.named_args)
        return p_locator

    @classmethod
    def convert_to_impl_with_locators(cls, *with_locators):
        out_list = []
        for locator in with_locators:
            l = isinstance(locator, ImplWith) and locator or locator.as_impl_locator()
            out_list.append(l)
        return out_list

    @classmethod
    def create_lmd(cls, *locators, meta=None):
        impl_locators = cls.convert_to_impl_with_locators(*locators)
        processed_locators = []
        for locator in impl_locators:
            ltype = locator.wtype.lower()
            if ltype == "content_locator":
                CONTENT_LOCATOR = cls.create_lmd(locator.wvalue)
                p_locator = Locator(ltype=locator.wtype, lvalue=CONTENT_LOCATOR, named_args=None)
            else:
                p_locator = cls.__process_single_raw_locator(locator)
            processed_locators.append(p_locator)
        return GuiElementMetaData(processed_locators, meta)

    @staticmethod
    def locators_as_str(locators):
        if not locators:
            return list()

        from arjuna.interact.gui.helpers import With
        out_list = []
        for l in locators:
            if isinstance(l, GuiGenericLocator) or isinstance(l, With):
                out_list.append(l.as_map())
            else:
                out_list.append(str(l))
        return out_list

class SimpleGuiElementMetaData(GuiElementMetaData):

    def __init__(self, locator_type, locator_value, named_args=dict()):
        super().__init__([Locator(ltype=locator_type, lvalue=locator_value, named_args=named_args)])
