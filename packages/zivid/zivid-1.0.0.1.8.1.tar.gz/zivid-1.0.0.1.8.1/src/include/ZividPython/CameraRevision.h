#pragma once

#include <Zivid/CameraRevision.h>
#include <ZividPython/Wrappers.h>

namespace ZividPython
{
    void wrapClass(pybind11::class_<Zivid::CameraRevision> pyClass);
} // namespace ZividPython
