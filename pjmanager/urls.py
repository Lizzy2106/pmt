from django.urls import path
from .views import user, team, type, projet, group, site

user_url = [
	path('user', user.list, name='userList'),
	path('user/trash', user.trash, name='trashUser'),
	path('user/<str:pk>/show', user.show, name='profile'),
	# path('user/<str:pk>/group', user.group, name='groupUser'),
	# path('user/<str:pk>/update', user.update, name='updateUser'),
	path('user/<str:pk>/destroy', user.destroy, name='destroyUser'),
	path('login', user.loginUser, name='login'),
	path('register', user.register, name='register'),
	path('logout', user.logoutUser, name='logout'),
	# Groups	
	path('user/group/<str:pk>/', user.add_groups, name='addGroup'),
]

group_url = [
	path('group', group.list, name='listGroup'),
	path('group/create', group.create, name='createGroup'),
	path('group/<str:pk>/show', group.show, name='showGroup'),
	path('group/<str:pk>/update', group.update, name='updateGroup'),
	path('group/<str:pk>/delete', group.destroy, name='destroyGroup'),
	# Permissions	
	path('perm/<str:group>/<str:perm>/', group.add_permissions, name='addPerm'),
	path('perm/<str:group>/<str:perm>/', group.rmv_permissions, name='rmvPerm'),
	path('perm/<str:group>/', group.clear_permissions, name='clearPerm'),
]

type_url = [
	path('type', type.list, name='listType'),
	path('type/trash', type.trash, name='trashType'),
	path('type/create', type.create, name='createType'),
	path('type/<str:pk>/show', type.show, name='showType'),
	path('type/<str:pk>/update', type.update, name='updateType'),
	path('type/<str:pk>/delete', type.destroy, name='destroyType'),
]


projet_url = [
	path('projet', projet.list, name='listProjet'),
	path('projet/trash', projet.trash, name='trashProjet'),
	path('projet/create', projet.create, name='createProjet'),
	path('projet/<str:pk>/show', projet.show, name='showProjet'),
	path('projet/<str:pk>/update', projet.update, name='updateProjet'),
	path('projet/<str:pk>/delete', projet.destroy, name='destroyProjet'),
]

team_url = [
	path('team', team.list, name='listTeam'),
	path('team/create', team.create, name='createTeam'),
	path('team/<str:pk>/add_user', team.add_user, name='addUserTeam'),
	path('team/<str:pk>/show', team.show, name='showTeam'),
	path('team/<str:pk>/update', team.update, name='updateTeam'),
	path('team/<str:pk>/delete', team.destroy, name='destroyTeam'),
]

history_url = [
	path('history', site.history, name='history'),
	path('history/<str:classe>/<str:pk>/show', site.obj_history, name='obj_history'),
	path('history/<str:classe>/<str:pk>/', site.one_history, name='one_history'),
	# path('team/<str:pk>/add_user', team.add_user, name='addUserTeam'),
]

urlpatterns = [
	path('', site.home, name='home'),
	path('search',site.search,name='search')
]

urlpatterns += user_url
urlpatterns += group_url
urlpatterns += type_url
urlpatterns += projet_url
urlpatterns += team_url
urlpatterns += history_url
