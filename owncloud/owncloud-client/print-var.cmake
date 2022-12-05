if(NOT TARGET_SCRIPT OR NOT TARGET_VAR)
    message(FATAL_ERROR "Required variable(s) not defined")
endif()

include(${TARGET_SCRIPT})
message("${${TARGET_VAR}}")
