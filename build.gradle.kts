import org.jetbrains.skiko.gradle.SkiaArchiveTask
import org.jetbrains.skiko.gradle.SkiaCompileTask
import de.undercouch.gradle.tasks.download.Download
import java.nio.file.Paths
import java.util.Locale

plugins {
    // we need this plugin for configuring Zip-derived dynamic tasks
    distribution
    id("de.undercouch.download") version("5.6.0")
}


fun skiaArchiveName(changeset: String) = "${changeset}"
fun skiaArchivePath(): String = rootProject.layout.buildDirectory.dir("skia-archive").get().toString()
fun skiaUnzippedPath(): String = rootProject.layout.buildDirectory.dir("skia").get().toString()
fun skiaChangeset() = project.properties["skia.changeset"] as String

val changeset = skiaChangeset()

tasks.register("skiaEnv") {
    group = "Download Skiko"
    description = "Print all skia-related environment properties"
    doLast {
        println("skia repository (-Pskia.repo)      ${project.properties["skia.repo"]}")
        println("skia changeset  (-Pskia.changeset) ${project.properties["skia.changeset"]}")
        println("skia archive \t\t\t   ${skiaArchivePath()}")
        println("skia unzipped \t\t\t   ${skiaUnzippedPath()}")
    }
}

val downloadSkiaAsArchive = tasks.register<Download>("skiaDownloadAsArchive") {
    group = "Download Skiko"
    description = "This tasks downloads skia repo"
    onlyIfModified(true)
    overwrite(false)
    src("${project.properties["skia.repo"]}/archive/${changeset}.zip")
    dest(skiaArchivePath())
}

val unarchiveSkia = tasks.register<Copy>("skiaUnarchive") {
    val source = Paths.get(downloadSkiaAsArchive.get().dest.absolutePath, skiaArchiveName(changeset) + ".zip")
    inputs.file(source)

    val outDir = skiaUnzippedPath()
    outputs.dir(Paths.get(outDir, skiaArchiveName(changeset)))

    group = "Download Skiko"
    dependsOn(downloadSkiaAsArchive)

    from(zipTree(source))
    into(outDir)
}

fun skiaWorkingDir() =
    Paths.get(
        unarchiveSkia.get().destinationDir.absolutePath,
        "skia-$changeset"
    ).toString()

fun skiaWorkingDir(subPath: String) =
    Paths.get(
        skiaWorkingDir(),
        subPath
    ).toString()

val skiaGitSyncDeps = tasks.register<Exec>("skiaGitSyncDeps") {
    group = "Download Skiko"
    description = "Sync Skia submodules"
    dependsOn(unarchiveSkia)

    standardOutput = System.out
    executable = "python3"

    workingDir(skiaWorkingDir())
    args("tools/git-sync-deps")
}

val skiaFetchNinja = tasks.register<Exec>("skiaFetchNinja") {
    group = "Download Skiko"
    description = "Fetch ninja"
    dependsOn(unarchiveSkia)

    outputs.file(skiaWorkingDir(Paths.get("third_party","ninja","ninja").toString()))

    standardOutput = System.out
    executable = "python3"

    workingDir(skiaWorkingDir())
    args("bin/fetch-ninja")
}

val skiaPrepare = tasks.register<Copy>("skiaPrepare") {
    dependsOn(skiaGitSyncDeps, skiaFetchNinja)
}


private fun createBuildTasks(): MutableList<TaskProvider<*>> {
    val artefactTasks = mutableListOf<TaskProvider<*>>()

    fun String.title() = replaceFirstChar {
        if (it.isLowerCase()) it.titlecase(
            Locale.getDefault()
        ) else it.toString()
    }

    listOf(
        Pair("android", "arm64"),
        Pair("android", "x64"),
        Pair("ios", "arm64"),
        Pair("ios", "x64"),
        Pair("iosSim", "arm64"),
        Pair("iosSim", "x64"),
        Pair("macos", "arm64"),
        Pair("macos", "x64"),
        Pair("windows", "arm64"),
        Pair("windows", "x64"),
        Pair("linux", "arm64"),
        Pair("linux", "x64"),
        Pair("wasm", "wasm"),
    ).forEach { (targetConfig, machineConfig) ->
        val buildTypeConfig = (project.properties["skia.build.type"] as? String) ?: "Release"

        val buildTask = tasks.register<SkiaCompileTask>("skiaBuild${targetConfig.title()}${machineConfig.title()}") {
            dependsOn(skiaPrepare)
            group = "Skia Build"

            skiaWorkingDir = skiaWorkingDir()
            buildType = buildTypeConfig
            target = targetConfig
            machine = machineConfig
        }

        val archiveTask = tasks.register<SkiaArchiveTask>("skiaArchive${targetConfig.title()}${machineConfig.title()}") {
            dependsOn(buildTask)

            inputs.files(buildTask.get().outputs.files)

            version = project.properties["skia.build.version"] as String?
                ?: throw GradleException("skia.build.version property is not set")

            group = "Skia Archive"
            buildType = buildTypeConfig
            target = targetConfig
            machine = machineConfig
            classifier = ""

            includeEmptyDirs = false

            val outDir = Paths.get("out",buildType.get() + '-' + target.get() + '-' + machine.get()).toString()

            from(skiaWorkingDir()) {
                include(
                    "$outDir/*.a",
                    "$outDir/*.lib",
                    "$outDir/icudtl.dat",
                    "include/**/*",
                    "modules/particles/include/*.h",
                    "modules/skottie/include/*.h",
                    "modules/skottie/src/*.h",
                    "modules/skottie/src/animator/*.h",
                    "modules/skottie/src/effects/*.h",
                    "modules/skottie/src/layers/*.h",
                    "modules/skottie/src/layers/shapelayer/*.h",
                    "modules/skottie/src/text/*.h",
                    "modules/skparagraph/include/*.h",
                    "modules/skplaintexteditor/include/*.h",
                    "modules/skresources/include/*.h",
                    "modules/sksg/include/*.h",
                    "modules/skshaper/include/*.h",
                    "modules/skshaper/src/*.h",
                    "modules/svg/include/*.h",
                    "modules/skcms/src/*.h",
                    "modules/skcms/*.h",
                    "modules/skunicode/include/*.h",
                    "modules/skunicode/src/*.h",
                    "src/base/*.h",
                    "src/core/*.h",
                    "src/gpu/gl/*.h",
                    "src/utils/*.h",
                    "third_party/externals/angle2/LICENSE",
                    "third_party/externals/angle2/include/**/*",
                    "third_party/externals/freetype/docs/FTL.TXT",
                    "third_party/externals/freetype/docs/GPLv2.TXT",
                    "third_party/externals/freetype/docs/LICENSE.TXT",
                    "third_party/externals/freetype/include/**/*",
                    "third_party/externals/icu/source/common/**/*.h",
                    "third_party/externals/libpng/LICENSE",
                    "third_party/externals/libpng/*.h",
                    "third_party/externals/libwebp/COPYING",
                    "third_party/externals/libwebp/PATENTS",
                    "third_party/externals/libwebp/src/dec/*.h",
                    "third_party/externals/libwebp/src/dsp/*.h",
                    "third_party/externals/libwebp/src/enc/*.h",
                    "third_party/externals/libwebp/src/mux/*.h",
                    "third_party/externals/libwebp/src/utils/*.h",
                    "third_party/externals/libwebp/src/webp/*.h",
                    "third_party/externals/harfbuzz/COPYING",
                    "third_party/externals/harfbuzz/src/*.h",
                    "third_party/externals/swiftshader/LICENSE.txt",
                    "third_party/externals/swiftshader/include/**/*",
                    "third_party/externals/zlib/LICENSE",
                    "third_party/externals/zlib/*.h",
                    "third_party/icu/*.h"
                )
            }


            val dist = "Skia-" + version.get() + "-" + target.get() + "-" + buildType.get() + "-" + machine.get() + classifier.get()
            archiveBaseName.set(dist)
        }

        val artefactTask = tasks.register("skiaBuildArtefact${targetConfig.title()}${machineConfig.title()}") {
            group = "Skia Build Artefact"
            dependsOn(buildTask, archiveTask)
        }

        artefactTasks.add(artefactTask)
    }

    return artefactTasks
}

project.getTasksByName("build", false).first().dependsOn(createBuildTasks())
