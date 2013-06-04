from ftw.upgrade import UpgradeStep


class UpdateDeleteAction(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-collective.deletepermission.upgrades:1001')
