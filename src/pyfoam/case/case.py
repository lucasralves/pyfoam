_types = [
    'incompressible-laminar',
    'incompressible-turbulent',
    'compressible-laminar',
    'compressible-turbulent',
]

_turbulent_models = [
    'kOmegaSST',
    'SpalartAllmaras',
]

_options = {

}

_options_kOmegaSST = {

}

_options_SpalartAllmaras = {
    
}

def create_case(path: str,
                type: str,
                options: dict) -> None:
    
    #---------------------------------------#
    # Check inputs
    #---------------------------------------#

    #---------------------------------------#
    # Copy case from data folder
    #---------------------------------------#

    #---------------------------------------#
    # Correct files
    #---------------------------------------#

    # 0 folder

    # constant folder

    # system folder

    return

def run_case(path: str,
             from_latest: bool = False) -> None:
    
    #---------------------------------------#
    # Find latest folder if necessary
    #---------------------------------------#

    #---------------------------------------#
    # Run
    #---------------------------------------#

    return