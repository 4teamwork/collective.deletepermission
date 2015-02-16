from ftw.builder.dexterity import DexterityBuilder
from ftw.builder import builder_registry


class DXFolderBuilder(DexterityBuilder):
    portal_type = 'dexterity.folder'

builder_registry.register('dexterity.folder', DXFolderBuilder)
