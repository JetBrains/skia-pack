package org.jetbrains.skiko.gradle

import org.gradle.api.provider.Property
import org.gradle.api.tasks.Exec
import org.gradle.api.tasks.Input
import org.gradle.api.Project
import org.gradle.api.tasks.bundling.Zip

private interface SkiaBuildTask {
    @get:Input
    val buildType: Property<String>

    @get:Input
    val target: Property<String>

    @get:Input
    val machine: Property<String>

    fun Project.scriptDir() = projectDir.resolve("script")
}

// https://docs.gradle.org/current/userguide/custom_tasks.html
abstract class SkiaCompileTask : Exec(), SkiaBuildTask {
    @get:Input
    abstract val skiaWorkingDir: Property<String>

    override fun exec() {

        standardOutput = System.out
        executable = "python3"
        args(
            project.scriptDir().resolve("build.py"),
            "--skia",
            skiaWorkingDir.get(),
            "--target",
            target.get(),
            "--build-type",
            buildType.get(),
            "--machine",
            machine.get()
        )
        println("Executing $executable  ${args?.joinToString(" ")}")
        super.exec()
    }
}

// https://docs.gradle.org/current/userguide/custom_tasks.html
abstract class SkiaArchiveTask : Zip(), SkiaBuildTask {
    @get:Input
    abstract val version: Property<String>

    @get:Input
    abstract val classifier: Property<String>
}
