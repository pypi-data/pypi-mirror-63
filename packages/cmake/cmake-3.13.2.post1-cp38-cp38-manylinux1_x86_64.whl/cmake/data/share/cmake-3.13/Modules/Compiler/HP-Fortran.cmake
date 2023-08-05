set(CMAKE_Fortran_VERBOSE_FLAG "-v")
set(CMAKE_Fortran_FORMAT_FIXED_FLAG "+source=fixed")
set(CMAKE_Fortran_FORMAT_FREE_FLAG "+source=free")

set(CMAKE_Fortran_CREATE_ASSEMBLY_SOURCE "<CMAKE_Fortran_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -S <SOURCE> -o <ASSEMBLY_SOURCE>")
set(CMAKE_Fortran_CREATE_PREPROCESSED_SOURCE "<CMAKE_Fortran_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -E <SOURCE> > <PREPROCESSED_SOURCE>")

set(CMAKE_Fortran_LINKER_WRAPPER_FLAG "-Wl,")
set(CMAKE_Fortran_LINKER_WRAPPER_FLAG ",")
