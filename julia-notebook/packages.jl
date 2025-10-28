using Pkg

dependencies = [
    "IJulia",
    "Oscar",
    "HomotopyContinuation",
    "DifferentialEquations",
    "SpeedyWeather"
]

for d in dependencies
    Pkg.add(d)
end

Pkg.instantiate()