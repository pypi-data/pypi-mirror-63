/*
 * MIT License
 *
 * Copyright (c) 2020 Hyeonki Hong <hhk7734@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include <gpiod.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#define LIBGPIODCXX_VERSION(a, b) (((a) << 8) + (b))

namespace py = pybind11;

PYBIND11_MODULE(_gpiod, m) {
    py::class_<gpiod::chip> chip(m, "chip");

    chip.def(py::init<>())
        .def(py::init<const std::string &>())
        .def(py::init<const std::string &, int>())
        .def("open",
             &gpiod::chip::open,
             py::arg("device"),
             py::arg("how") = int(gpiod::chip::OPEN_LOOKUP))
        .def("reset", &gpiod::chip::reset)
        .def("name", &gpiod::chip::name)
        .def("label", &gpiod::chip::label)
        .def("num_lines", &gpiod::chip::num_lines)
        .def("get_line", &gpiod::chip::get_line, py::arg("offset"))
        .def("find_line", &gpiod::chip::find_line, py::arg("name"));

    chip.attr("OPEN_LOOKUP")    = int(gpiod::chip::OPEN_LOOKUP);
    chip.attr("OPEN_BY_PATH")   = int(gpiod::chip::OPEN_BY_PATH);
    chip.attr("OPEN_BY_NAME")   = int(gpiod::chip::OPEN_BY_NAME);
    chip.attr("OPEN_BY_LABEL")  = int(gpiod::chip::OPEN_BY_LABEL);
    chip.attr("OPEN_BY_NUMBER") = int(gpiod::chip::OPEN_BY_NUMBER);


    py::class_<gpiod::line_request> line_request(m, "line_request");

    line_request.attr("DIRECTION_AS_IS")
        = int(gpiod::line_request::DIRECTION_AS_IS);
    line_request.attr("DIRECTION_INPUT")
        = int(gpiod::line_request::DIRECTION_INPUT);
    line_request.attr("DIRECTION_OUTPUT")
        = int(gpiod::line_request::DIRECTION_OUTPUT);
    line_request.attr("EVENT_FALLING_EDGE")
        = int(gpiod::line_request::EVENT_FALLING_EDGE);
    line_request.attr("EVENT_RISING_EDGE")
        = int(gpiod::line_request::EVENT_RISING_EDGE);
    line_request.attr("EVENT_BOTH_EDGES")
        = int(gpiod::line_request::EVENT_BOTH_EDGES);

    line_request.def(py::init<>())
        .def_readwrite("consumer", &gpiod::line_request::consumer)
        .def_readwrite("request_type", &gpiod::line_request::request_type)
        .def_readwrite("flags", &gpiod::line_request::flags);


    py::class_<gpiod::line> line(m, "line");

    line.def(py::init<>())
        .def("offset", &gpiod::line::offset)
        .def("name", &gpiod::line::name)
        .def("consumer", &gpiod::line::consumer)
        .def("direction", &gpiod::line::direction)
        .def("active_state", &gpiod::line::active_state)
#if LIBGPIODCXX_VERSION_CODE >= LIBGPIODCXX_VERSION(1, 5)
        .def("bias", &gpiod::line::bias)
#endif
        .def("is_used", &gpiod::line::is_used)
        .def("is_open_drain", &gpiod::line::is_open_drain)
        .def("is_open_source", &gpiod::line::is_open_source)
        .def("request",
             &gpiod::line::request,
             py::arg("config"),
             py::arg("default_val") = 0)
        .def("release", &gpiod::line::release)
        .def("is_requested", &gpiod::line::is_requested)
        .def("get_value", &gpiod::line::get_value)
        .def("set_value", &gpiod::line::set_value, py::arg("value"))
#if LIBGPIODCXX_VERSION_CODE >= LIBGPIODCXX_VERSION(1, 5)
        .def("set_config",
             &gpiod::line::set_config,
             py::arg("direction"),
             py::arg("flags"),
             py::arg("value") = 0)
        .def("set_flags", &gpiod::line::set_flags, py::arg("flags"))
        .def("set_direction_input", &gpiod::line::set_direction_input)
        .def("set_direction_output",
             &gpiod::line::set_direction_output,
             py::arg("value") = 0)
#endif
        .def("event_wait", &gpiod::line::event_wait, py::arg("timeout_ns"))
        .def("event_read", &gpiod::line::event_read)
#if LIBGPIODCXX_VERSION_CODE >= LIBGPIODCXX_VERSION(1, 5)
        .def("event_read_multiple", &gpiod::line::event_read_multiple)
#endif
        .def("event_get_fd", &gpiod::line::event_get_fd)
        .def("get_chip", &gpiod::line::get_chip)
#if LIBGPIODCXX_VERSION_CODE >= LIBGPIODCXX_VERSION(1, 5)
        .def("update", &gpiod::line::update)
#endif
        .def("reset", &gpiod::line::reset);

    line.attr("DIRECTION_INPUT")  = int(gpiod::line::DIRECTION_INPUT);
    line.attr("DIRECTION_OUTPUT") = int(gpiod::line::DIRECTION_OUTPUT);
    line.attr("ACTIVE_LOW")       = int(gpiod::line::ACTIVE_LOW);
    line.attr("ACTIVE_HIGH")      = int(gpiod::line::ACTIVE_HIGH);
#if LIBGPIODCXX_VERSION_CODE >= LIBGPIODCXX_VERSION(1, 5)
    line.attr("BIAS_AS_IS")     = int(gpiod::line::BIAS_AS_IS);
    line.attr("BIAS_DISABLE")   = int(gpiod::line::BIAS_DISABLE);
    line.attr("BIAS_PULL_UP")   = int(gpiod::line::BIAS_PULL_UP);
    line.attr("BIAS_PULL_DOWN") = int(gpiod::line::BIAS_PULL_DOWN);
#endif


    m.def("find_line", &gpiod::find_line, py::arg("name"));


    py::class_<gpiod::line_event> line_event(m, "line_event");

    line_event.attr("RISING_EDGE")  = int(gpiod::line_event::RISING_EDGE);
    line_event.attr("FALLING_EDGE") = int(gpiod::line_event::FALLING_EDGE);

    line_event.def(py::init<>())
        .def_readwrite("timestamp", &gpiod::line_event::timestamp)
        .def_readwrite("event_type", &gpiod::line_event::event_type)
        .def_readwrite("source", &gpiod::line_event::source);


    py::class_<gpiod::line_bulk> line_bulk(m, "line_bulk");

    line_bulk.def(py::init<>())
        .def(py::init<const std::vector<gpiod::line> &>())
        .def("append", &gpiod::line_bulk::append, py::arg("new_line"))
        .def("get", &gpiod::line_bulk::get, py::arg("offset"))
        .def("size", &gpiod::line_bulk::size)
        .def("empty", &gpiod::line_bulk::empty)
        .def("clear", &gpiod::line_bulk::clear)
        .def("request",
             &gpiod::line_bulk::request,
             py::arg("config"),
             py::arg("default_vals") = std::vector<int>())
        .def("release", &gpiod::line_bulk::release)
        .def("get_values", &gpiod::line_bulk::get_values)
        .def("set_values", &gpiod::line_bulk::set_values, py::arg("values"))
        .def(
            "event_wait", &gpiod::line_bulk::event_wait, py::arg("timeout_ns"));

    py::class_<gpiod::line_bulk::iterator> iterator(line_bulk, "iterator");

    iterator.def(py::init<>());

    line_bulk.def("begin", &gpiod::line_bulk::begin)
        .def("end", &gpiod::line_bulk::end);


    m.def("make_chip_iter", &gpiod::make_chip_iter)
        .def("begin",
             py::overload_cast<gpiod::chip_iter>(&gpiod::begin),
             py::arg("iter"))
        .def("end",
             py::overload_cast<const gpiod::chip_iter &>(&gpiod::end),
             py::arg("iter"));


    py::class_<gpiod::chip_iter> chip_iter(m, "chip_iter");

    chip_iter.def(py::init<>());


    m.def("begin",
           py::overload_cast<gpiod::line_iter>(&gpiod::begin),
           py::arg("iter"))
        .def("end",
             py::overload_cast<const gpiod::line_iter &>(&gpiod::end),
             py::arg("iter"));


    py::class_<gpiod::line_iter> line_iter(m, "line_iter");

    line_iter.def(py::init<>());
}