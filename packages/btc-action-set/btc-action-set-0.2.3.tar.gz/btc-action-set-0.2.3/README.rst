===================================================
BTC Action Set
===================================================

Features for managing template elements depending on the project role and permission system.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "action_set" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'action_set',
      )

2. `ActionSet`. Prepare base action-set, for example we'll use built-in `ActionSetWithPermissionCheck`::

    class BaseActionSet(ActionSetWithPermissionCheck):

        protect_css_class: str = 'protected-element'
        elements_permissions = {
            'action_1': ['change_status'],  # - for search in user permissions
            'action_2': ['edit']
        }

        def get_user_permissions(self) -> list:
            return User.objects.filter(pk=self.request.user.pk).values_list('user_roles__permissions__name', flat=True)

        def check_permissions(self) -> None:
            if not self.request.user.is_superuser:
                return super().check_permissions()

3. Write custom action-set::

    class MyActionSet(BaseActionSet):

        template = 'action_set/my_action_set.html'

        action_1 = ActionButton(
            'Action 1', css_classes=['js-post_content_btn'],
            html_params={
                'type': 'button',
                'data-url': reverse('app:action_1'),
            }
        )
        action_2 = ActionButton(
            'Action 2', css_classes=['js-load_content_btn'],
            html_params={
                'type': 'button'
            }
        )

        def __init__(self, instance, *args, **kwargs)
            self.instance = instance  # type: MyModel
            super().__init__(*args, **kwargs)
            self.actions['action_2'].html_params.update({'data-url': reverse('app:action_2', self.instance.pk)})

4. Write view, use `ActionSetMixinView` to construct view::

    class MyViewWithActionSet(ActionSetMixinView, TemplateView):
        ...
        template_name = 'my_view_template.html'
        action_set_class = MyActionSet
        ...

        def get_action_set_kwargs(self, **kwargs) -> dict:
            return super().get_action_set_kwargs(instance=get_object_or_404(MyModel, pk=self.kwargs['pk']), **kwargs)

5. Prepare template::

    <!-- action_set/my_action_set.html -->
    ...
    <div class="action-set action-set__my-action-set">
        <div class="action-set__info">
            <i class="material-icons">landscape</i>
            <span>Action Set Test</span>
        </div>
        <div class="action-set__toolbar">
            {% for action in action_set %}
                {{ action }}
            {% endfor %}
        </div>
    </div>
    ...

6. In the template of the view call `render` method::

    <!-- my_view_template.html -->
    ...
    <div>{{ action_set.render }}</div>
    ...

7. `ActionSetGroup`. Setup group and instantiate action-sets::

    class CustomActionSetGroup(ActionSetGroup):

        action_set_1 = MyActionSet1
        action_set_2 = MyActionSet2

8. Use `ActionSetGroupMixinView` to construct custom mixin and view like we did it with `ActionSetMixinView`.
   Next setup is same as for the `ActionSet`::

    class MyView(CustomActionSetGroupMixinView, TemplateView):

        action_set_group_class = CustomActionSetGroup
        template_name = 'my_awesome_page.html'

9. In template::

    ...
    <div>
        {{ action_set_group.action_set_1.render }}
    </div>
    <div>
        {{ action_set_group.action_set_2.render }}
    </div>
    ...

10 `ActionSetMenuMixin`. You can building menus by using `ActionSetMenuMixin` (automatic tabs highlight support).
Note: prepare template as was shown for the simple ActionSet::

    class MyDetailsMenu(ActionSetMenuMixin, ActionSet or use ActionSetWithPermissionCheck):

        url_attribute_name: str = 'data-url'       # attribute for comparing with current request.path
        activate_class: str = 'active'             # class for active button
        template = 'action_set/details_menu.html'

        menu_tab_1 = ActionButton(
            'TAB1', css_classes=['js-menu-btn'],
            html_params={
                'type': 'button',
                'data-container': '.js-my_content',
                'data-url': reverse_lazy('app:tab_1')
            }
        )
        menu_tab_2 = ActionButton(
            'TAB2', css_classes=['js-menu-btn'],
            html_params={
                'type': 'button',
                'data-container': '.js-my_content',
                'data-url': reverse_lazy('app:tab_2')
            }
        )
        # ... etc.

11 `BreadcrumbsSet`. You can use this Action Set for building breadcrumbs. Prepare custom `BreadcrumbsSet`::

    class MyBreadcrumbsSet(BreadcrumbsSet):

        template = 'my_breadcrumbs.html'
        active_crumb_css_class = 'active-breadcrumb'     # for highlight

        crumb1 = ActionButton(
            'Crumb1',
            html_params={
                'data-url': reverse_lazy('app:tab1'),
                'data-container': '.js-dispatcher-content'
            }
        )
        crumb2 = ActionButton(
            'Crumb2',
            html_params={
                'data-url': reverse_lazy('app:tab2'),
                'data-container': '.js-dispatcher-content'
            }
        )
        # ... etc.

12 Prepare yor view for showing breadcrumbs - use `BreadcrumbsMixinView`::

    class MyView(BreadcrumbsMixinView, TemplateView):

        breadcrumbs_set_class = MyBreadcrumbsSet
        template_name = 'my_awesome_page.html'

        breadcrumbs_set = ['crumb1', '*crumb2']  # use '*' symbol for showing active breadcrumb.


13 Prepare template::

    <!-- my_breadcrumbs.html -->

    {% load dev_tools %}

    <div class="action-set action-set__breadcrumbs">
        {% for action in action_set %}
            {{ action|tweak_parameter:'class: mdl-button' }}
            {% if not forloop.last %}
                <span class="breadcrumbs-separator">></span>
            {% endif %}
        {% endfor %}
    </div>
