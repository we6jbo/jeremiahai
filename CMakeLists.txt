cmake_minimum_required(VERSION 3.21)

project(jeremiahai VERSION 1.4.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

qt_add_executable(jeremiahai
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
    resources.qrc
)

target_link_libraries(jeremiahai PRIVATE Qt6::Widgets)

install(TARGETS jeremiahai RUNTIME DESTINATION bin)

# Flathub desktop integration
install(FILES org.oneal.jeremiahai.desktop
        DESTINATION share/applications)
install(FILES org.oneal.jeremiahai.metainfo.xml
        DESTINATION share/metainfo)
install(FILES org.oneal.jeremiahai.svg
        DESTINATION share/icons/hicolor/scalable/apps)
