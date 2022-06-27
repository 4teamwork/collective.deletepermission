from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder


class DXFolderBuilder(DexterityBuilder):
    portal_type = 'dxfolder'

builder_registry.register('dxfolder', DXFolderBuilder)
