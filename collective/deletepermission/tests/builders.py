from ftw.builder.dexterity import DexterityBuilder
from ftw.builder import builder_registry


class DXFolderBuilder(DexterityBuilder):
    portal_type = 'dxfolder'

builder_registry.register('dxfolder', DXFolderBuilder)
