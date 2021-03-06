# -*- coding: utf-8 -*-

from gluon.sqlhtml import FormWidget
from gluon.sqlhtml import UploadWidget

# ----------------------------------------------------------------------------------------------------------------------
# dal represent/format helpers
# ----------------------------------------------------------------------------------------------------------------------
# https://mkaz.tech/python-string-format.html
# https://pyformat.info/#number


def dal_represent_number(v, r):
    return "{:,}".format(v) if v is not None else v


def dal_represent_percent(v, r):
    return "{:.2%}".format(v / 100) if v is not None else v


# https://regex101.com/
# http://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number
dal_regex_phone_num = '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'
dal_regex_na_phone_num = '^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$'
dal_regex_ssn = '^\d{3}-\d{2}-\d{4}$'

dal_list_genders = [('F', 'Female'), ('M', 'Male')]
dal_list_booleans = [('Y', 'Yes'), ('N', 'No')]

dal_list_states = [
    ('AL', 'Alabama, USA'),
    ('AK', 'Alaska, USA'),
    ('AB', 'Alberta, CAN'),
    ('AS', 'American Samoa, USA'),
    ('AZ', 'Arizona, USA'),
    ('AR', 'Arkansas, USA'),
    ('BC', 'British Columbia, CAN'),
    ('CA', 'California, USA'),
    ('CO', 'Colorado, USA'),
    ('CT', 'Connecticut, USA'),
    ('DE', 'Delaware, USA'),
    ('FL', 'Florida, USA'),
    ('GA', 'Georgia, USA'),
    ('GU', 'Guam, USA'),
    ('HI', 'Hawaii, USA'),
    ('ID', 'Idaho, USA'),
    ('IL', 'Illinois, USA'),
    ('IN', 'Indiana, USA'),
    ('IA', 'Iowa, USA'),
    ('KS', 'Kansas, USA'),
    ('KY', 'Kentucky, USA'),
    ('LA', 'Louisiana, USA'),
    ('ME', 'Maine, USA'),
    ('MB', 'Manitoba, CAN'),
    ('MD', 'Maryland, USA'),
    ('MA', 'Massachusetts, USA'),
    ('MI', 'Michigan, USA'),
    ('MN', 'Minnesota, USA'),
    ('MS', 'Mississippi, USA'),
    ('MO', 'Missouri, USA'),
    ('MT', 'Montana, USA'),
    ('NE', 'Nebraska, USA'),
    ('NV', 'Nevada, USA'),
    ('NB', 'New Brunswick, CAN'),
    ('NH', 'New Hampshire, USA'),
    ('NJ', 'New Jersey, USA'),
    ('NM', 'New Mexico, USA'),
    ('NY', 'New York, USA'),
    ('NL', 'Newfoundland and Labrador, CAN'),
    ('NC', 'North Carolina, USA'),
    ('ND', 'North Dakota, USA'),
    ('MP', 'Northern Mariana Islands, USA'),
    ('NT', 'Northwest Territories, CAN'),
    ('NS', 'Nova Scotia, CAN'),
    ('NU', 'Nunavut, CAN'),
    ('OH', 'Ohio, USA'),
    ('OK', 'Oklahoma, USA'),
    ('ON', 'Ontario, CAN'),
    ('OR', 'Oregon, USA'),
    ('PA', 'Pennsylvania, USA'),
    ('PE', 'Prince Edward Island, CAN'),
    ('PR', 'Puerto Rico, USA'),
    ('QC', 'Quebec, CAN'),
    ('RI', 'Rhode Island, USA'),
    ('SK', 'Saskatchewan, CAN'),
    ('SC', 'South Carolina, USA'),
    ('SD', 'South Dakota, USA'),
    ('TN', 'Tennessee, USA'),
    ('TX', 'Texas, USA'),
    ('VI', 'U.S. Virgin Islands, USA'),
    ('UT', 'Utah, USA'),
    ('VT', 'Vermont, USA'),
    ('VA', 'Virginia, USA'),
    ('WA', 'Washington, USA'),
    ('DC', 'Washington DC, USA'),
    ('WV', 'West Virginia, USA'),
    ('WI', 'Wisconsin, USA'),
    ('WY', 'Wyoming, USA'),
    ('YT', 'Yukon Territory, CAN'),
]


class Titleize(object):
    '''Field(..., requires=Titleize())'''

    def __call__(self, value):
        # return (value.title(), None)
        articles = ('in', 'the', 'a', 'an', 'of', 'is')
        return (' '.join([w if w in articles else w.title() if w.islower() else w for w in value.split()]), None)


# ----------------------------------------------------------------------------------------------------------------------
# custom forms
# https://groups.google.com/d/msg/web2py/1yCGgKANssE/MvOL4mUqRQ4J
# ----------------------------------------------------------------------------------------------------------------------

def widget(type='string', placeholder=''):
    '''Allow Field('name', widget=widget('string', 'my placeholder text'))'''
    # https://groups.google.com/d/msg/web2py/CTsUjEFUcR4/Vy-wIekEBAAJ
    # could also do https://groups.google.com/d/msg/web2py/VSr2oLNnozg/5AlMTNzdGgkJ
    return lambda field, value: SQLFORM.widgets[type].widget(field, value, _placeholder=placeholder)


def datepicker_widget(placeholder='', **settings):
    '''Datepicker plugin widget, also see in starter.js'''

    def widget(field, value, **attributes):

        default = {'_value': value}

        attributes = FormWidget._attributes(field, default, **attributes)
        attributes['_class'] = 'form-control date'

        data_attributes = {}
        data_attributes['date-format'] = 'dd.mm.yyyy'
        data_attributes['date-week-start'] = 1
        data_attributes['date-calendar-weeks'] = True
        for item in settings.items():
            data_attributes['date-'+item[0].replace('_', '-')] = item[1]

        return INPUT(
            data=data_attributes,
            _placeholder=placeholder,
            **attributes
        )

    return widget


def clockpicker_widget(placeholder='', **settings):
    '''Clockpicker plugin widget, also see in starter.js'''

    def widget(field, value, **attributes):

        default = {'_value': value}
        attributes = FormWidget._attributes(field, default, **attributes)
        attributes['_class'] = 'form-control time'

        data_attributes = {}
        for item in settings.items():
            data_attributes[item[0].replace('_', '-')] = item[1]

        return INPUT(
            data=data_attributes,
            _placeholder=placeholder,
            **attributes
        )

    return widget


def upload_image_widget(**settings):
    """Custom upload image widget with bootstrap style button and responsive image thumbnail
    """

    response.files.insert(1, URL('static', 'plugins/croppie/croppie.css'))
    response.files.insert(2, URL('static', 'plugins/croppie/croppie.min.js'))
    response.files.insert(3, URL('static', 'plugins/croppie/upload_image_widget.js'))

    def widget(field, value, download_url=None, **attributes):
        """Generates an INPUT file tag.

        Optionally provides an A link to the file, including a checkbox so
        the file can be deleted.

        All is wrapped in a DIV.

        see also: `FormWidget.widget`

        Args:
            field: the field
            value: the field value
            download_url: url for the file download (default = None)
        """

        modal = XML("""
        <div class="modal" id="croppie-modal" tabindex="-1" role="dialog" aria-labelledby="croppie-label">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title" id="croppie-label">Edit image</h4>
              </div>
              <div class="modal-body">
                <div id="croppie" style="margin: 0 auto;" class="center-block"></div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" data-dismiss="modal" id="croppie-result">Save changes</button>
              </div>
            </div>
          </div>
        </div>
        """)

        # Input button styling
        # https://stackoverflow.com/questions/11235206/twitter-bootstrap-form-file-element-upload-button
        default = dict(
            _type='file',
            _style='display: none',
            _onchange="$('#upload-file-info').html(this.files[0].name);"
                      "initCroppie(this);"
        )
        attributes = UploadWidget._attributes(field, default, **attributes)

        inp = DIV(
            LABEL('Choose image...', INPUT(**attributes), _class='btn btn-default', _for=attributes['_id'], _role='button'),
            SPAN(_class='label label-default', _id='upload-file-info', _style='margin-left: 5px;'),
        )

        if download_url and value:
            if not UploadWidget.is_image(value):
                raise Exception('Only images supported: set validator for the field "requires = IS_IMAGE()"')

            if callable(download_url):
                url = download_url(value)
            else:
                url = f'{download_url}/{value}'
            delete_button, image_label, br = '', '', ''
            image = IMG(_src=url, _height='40px', _class='img-responsive')

            requires = attributes["requires"]

            # Add delete button if image upload field may be empty
            if requires == [] or isinstance(requires, IS_EMPTY_OR):
                br = BR()
                # Delete image button changes #image-label html content
                delete_button = LABEL(INPUT(_type='checkbox',
                                            _style='display: none',
                                            _name=field.name + UploadWidget.ID_DELETE_SUFFIX,
                                            _id=field.name + UploadWidget.ID_DELETE_SUFFIX),
                                      I(_class='fa fa-times'),
                                      _class='btn btn-danger btn-sm pull-right',
                                      _role='checkbox',
                                      _title='Delete',
                                      _autocomplete='off',
                                      _style='border: 0;',
                                      _onmouseup="var img=$('#image-label'); "
                                                 "if (img.html()==='') "
                                                 "{img.html('Marked to delete');} "
                                                 "else {img.html('');}",
                                      data={'toggle': 'input'})
                image_label = LABEL(_id='image-label', _class='label label-danger')

            inp = DIV(
                inp,
                BR(),
                DIV(
                    DIV(
                        delete_button,
                        # Download image button
                        A(I(_class='glyphicon glyphicon-cloud-download'),
                          _href=url,
                          _class='btn btn-primary btn-sm pull-right',
                          _role='button',
                          _title='Download',
                          _style='margin-right: 5px; border: 0;',
                          ),
                        br,
                        image_label,
                        _class='box-header box-tools pull-right',
                    ),
                    DIV(image, _class='box-body'),
                    _class='box box-solid',
                ),
            )

        return DIV(modal, inp)

    return widget


def upload_image_represent(**settings):
    """Custom image represent function with responsive image thumbnail
    """

    def represent(field, value, download_url=None):
        """How to represent the file:

        - with download url and if it is an image: <A href=...><IMG ...></A>
        - otherwise with download url: <A href=...>file</A>
        - otherwise: file

        Args:
            field: the field
            value: the field value
            download_url: url for the file download (default = None)
        """

        inp = current.T(UploadWidget.GENERIC_DESCRIPTION)

        if download_url and value:
            if callable(download_url):
                url = download_url(value)
            else:
                url = download_url + '/' + value
            if UploadWidget.is_image(value):
                inp = IMG(_src=url, _height='40px', _class='img-responsive img-thumbnail')
            inp = A(inp, _href=url)

        return inp

    return represent


# ----------------------------------------------------------------------------------------------------------------------
# Sidebar menu
# ----------------------------------------------------------------------------------------------------------------------
def sidebar_menu_item(label, url=None, icon='link'):
    '''
    <li><a href="{{=URL('default','about')}}"><i class="fa fa-book"></i> <span>About</span></a></li>
    <a href="#"><i class="fa fa-gears"></i> <span>Admin</span> <i class="fa fa-angle-left pull-right"></i></a>
    '''

    if url:
        active = 'active' if url == URL() else None
        return LI(
            A(
                (I(' ', _class='fa fa-%s' % icon), SPAN(T(label))),
                _href=url
            ),
            _class=active
        )
    else:
        return A(
            (
                I(' ', _class='fa fa-%s' % icon),
                SPAN(T(label)),
                SPAN(
                    I(
                        ' ', 
                        _class='fa fa-angle-left pull-right'
                        ),
                    _class='pull-right-container'
                    )
            ),
            _href="#"
        )


# this is the main application menu add/remove items as required
# original response menu in layout.html
#
#
# def menu_item(label, controller, action, icon='link', args=[], user_signature=False, submenu=[]):
#     link = URL(controller, action, args=args, user_signature=user_signature)
#     menu_item = ((I(' ', _class='fa fa-%s' % icon), T(label)), link == URL(), link, submenu)
#     return menu_item
#
#
# response.menu = [
#     menu_item('Home', 'default', 'index', icon='home'),
#     menu_item('People', 'person', 'list', icon='home'),
#     menu_item('Dogs', 'dog', 'list', icon='home'),
#     menu_item('Dog Owners', 'dog_owner', 'list', icon='home'),
# ]


# ----------------------------------------------------------------------------------------------------------------------
# User helpers
# ----------------------------------------------------------------------------------------------------------------------
def is_user_member(*roles):
    # @auth.requires(lambda: is_user_member('arg', 'list', 'of', 'roles')
    # if is_user_member('arg', 'list', 'of', 'roles'):

    # @auth.requires(lambda: any([auth.has_membership(r) for r in ['list', 'of', 'roles'])) # db lookups!?
    # if auth.user and any(auth.has_membership(r) for r in ['customer_service', 'admin']): # performs potentially 4 database queries
    # if auth.has_membership('customer_service'): # performs two database
    # restrict menu options based on membership
    # https://groups.google.com/d/msg/web2py/bz-mKIFqP1w/eEma0XOyCAAJ
    # https://groups.google.com/forum/#!searchin/web2py/response.menu$20auth.user_id$20auth.has_membership/web2py/E8Krnt9cxB8/xSpuPy8d6M4J
    # https://groups.google.com/forum/#!searchin/web2py/response.menu$20auth.user_id$20auth.has_membership/web2py/GvDAXRIpKA0/sEcPeB8a40oJ
    # https://groups.google.com/forum/#!topic/web2py/8AHYqV_EKy0

    user_auth_groups = [x.lower() for x in auth.user_groups.values()]
    required_auth_groups = [x.lower() for x in roles]

    if auth.user and any(role in required_auth_groups for role in user_auth_groups):
        return True
    else:
        return False


def user_visibility(*groups):
    """in views, in class attribute: {{=user_visibility('list', 'of', 'authorized', 'user_groups')}}"""
    return 'hidden' if not is_user_member(*groups) else 'visible'


def user_photo(user):
    """
    Return user photo or default avatar based on user gender
    :param user: db.auth_user.row
    :return: path to user photo file
    """

    if user.photo:
        return URL('default', 'download', args=user.photo)
    elif user.sex:
        return URL('static', f'img/avatar_{user.sex.lower()}_1.png')
    else:
        return URL('static', 'img/boxed_bg.png')
