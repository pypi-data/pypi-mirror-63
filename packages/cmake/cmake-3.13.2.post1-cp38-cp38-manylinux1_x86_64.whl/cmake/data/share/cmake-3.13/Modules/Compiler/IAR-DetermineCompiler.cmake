# IAR Systems compiler for embedded systems.
#   http://www.iar.com
#   http://supp.iar.com/FilesPublic/UPDINFO/004916/arm/doc/EWARM_DevelopmentGuide.ENU.pdf
#
# __IAR_SYSTEMS_ICC__ An integer that identifies the IAR compiler platform:
#                       9 and higher means C11 and C++14 as language default
#                       8 means C99 and C++03 as language default
#                       7 and lower means C89 and EC++ as language default.
# __ICCARM__          An integer that is set to 1 when the code is compiled with the IAR C/C++ Compiler for ARM
# __VER__             An integer that identifies the version number of the IAR compiler in use. For example,
#                     version 5.11.3 is returned as 5011003.

set(_compiler_id_pp_test "defined(__IAR_SYSTEMS_ICC__) || defined(__IAR_SYSTEMS_ICC)")

set(_compiler_id_version_compute "
# if defined(__VER__)
#  define @PREFIX@COMPILER_VERSION_MAJOR @MACRO_DEC@((__VER__) / 1000000)
#  define @PREFIX@COMPILER_VERSION_MINOR @MACRO_DEC@(((__VER__) / 1000) % 1000)
#  define @PREFIX@COMPILER_VERSION_PATCH @MACRO_DEC@((__VER__) % 1000)
#  define @PREFIX@COMPILER_VERSION_INTERNAL @MACRO_DEC@(__IAR_SYSTEMS_ICC__)
# endif")
