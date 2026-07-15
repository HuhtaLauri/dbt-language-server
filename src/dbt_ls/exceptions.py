class DbtLsError(Exception):
    pass


class NoRootPathError(DbtLsError):
    pass


class NoDbtRootError(DbtLsError):
    pass


class NoDbtProfileError(DbtLsError):
    pass


class NoDbtProfileTargetError(DbtLsError):
    pass
