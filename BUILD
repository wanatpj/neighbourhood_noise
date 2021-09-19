load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "record_noise",
    srcs = ["record_noise.py"],
    main = "record_noise.py",
    deps = [
        requirement("numpy"),
        requirement("scipy"),
        requirement("sounddevice"),
    ],
)