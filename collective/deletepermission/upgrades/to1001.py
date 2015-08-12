
def upgrade(setup_context):
    setup_context.runImportStepFromProfile(
        'profile-collective.deletepermission.upgrades:1001',
        'actions',
        run_dependencies=False,
        purge_old=False)
