collective.deletepermission
===========================

The default Plone permission for deleting content does not allow to delete
content from a folder without being able to delete the folder itself.

The `collective.deletepermission` package introduces an additional permission
``Delete portal content``. By seperating the permission ``Delete portal
content`` (I can delete this content object)  from the permission ``Delete
objects`` (I can delete something IN this folder), we now can allow a
``Contributor`` to delete content he created (``Owner`` role) without letting
him delete folders and objects belonging to other users - even in a nested
environment.


Implementation details
----------------------

This package monkey patches:

- ``manage_delObjects`` of AT BaseFolder

- ``manage_cutObjects__roles__`` of AT BaseFolderMixin

- ``cb_userHasCopyOrMovePermissionchecks`` of OFS CopySupport

and overrides the following templates and scripts (skins):

- ``folder_rename_form.cpt``

- ``object_rename.py``

to implement a new ``Delete portal content`` permission.


The ``Delete portal content`` permission is now required on the object you want
to delete.
On parent objects the ``Delete objects`` permission is still required.
This gives us some more flexibility and makes it possible for a contributor to
delete his own content but nothing else. On the graph below you can see the
situation with the default permission settings and if it is deletable by
Contributor1.

::

  - Rootfolder of Admin (not deletable)
    '- Document of Contributor1 (deletable)
    '- Subfolder of Admin (not deletable)
      '- Document of Contributor1 (deletable)
      '- Document of Contrubutor2 (not deletable)

In default Plone this would look like this::

  - Rootfolder of Admin (not deletable)
    '- Document of Contributor1 (deletable)
    '- Subfolder of Admin (deletable)
      '- Document of Contributor1 (deletable)
      '- Document of Contrubutor2 (deletable)

This is caused by the fact that in default Plone we require the same permission
on the parent and the object.
If we have two levels where we should be able to delete some files, we always
end up with the user being able to delete the container of the second level.


Usage
-----

- Add ``collective.deletepermission`` to your buildout configuration:

::

    [instance]
    eggs +=
        collective.deletepermission

- Install the generic setup import profile.

Links
-----

- Main github project repository: https://github.com/4teamwork/collective.deletepermission
- Issue tracker: https://github.com/4teamwork/collective.deletepermission/issues
- Package on pypi: http://pypi.python.org/pypi/collective.deletepermission
- Continuous integration: https://jenkins.4teamwork.ch/search?q=collective.deletepermission


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``collective.deletepermission`` is licensed under GNU General Public License,
version 2.
