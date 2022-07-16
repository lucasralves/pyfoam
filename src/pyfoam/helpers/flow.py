_R = 287.5
_gamma = 1.4

def sound_speed(method: str, **kargs) -> float:
    """
    How to use it:
    --------------

    temp = sound_speed("temperature", temperature=300) # [K]
    temp = sound_speed("pressure-density", pressure=101325, density=1.225) # [Pa, kg/m^3]

    """
    return

def ideal_gas(parameter: str, **kargs) -> float:
    """
    How to use it:
    --------------

    temp = ideal_gas("temperature", pressure=101325, density=1.225) # [Pa, kg/m^3]
    p = ideal_gas("pressure", temperature=300, density=1.225) # [K, kg/m^3]
    rho = ideal_gas("density", pressure=101325, temperature=300) # [Pa, K]
    
    """
    return

def viscosity(temperature: float) -> float:
    return

def mach(velocity: float, air_speed: float) -> float:
    return velocity / air_speed

def reynolds(velocity: float, density: float, viscosity: float, ref_lenght: float) -> float:
    return velocity * density * ref_lenght / viscosity