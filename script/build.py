#! /usr/bin/env python3

import common, os, subprocess, sys
from checkout import chdir_home

def main():
  chdir_home()

  build_type = common.build_type()
  machine = common.machine()
  host = common.host()
  host_machine = common.host_machine()
  target = common.target()
  ndk = common.ndk()
  is_win = common.windows()
  is_mingw = "mingw" == host

  tools_dir = "depot_tools"
  ninja = 'ninja.exe' if is_win else 'ninja'
  isIos = 'ios' == target or 'iosSim' == target
  isIosSim = 'iosSim' == target

  if build_type == 'Debug':
    args = ['is_debug=true']
  else:
    args = ['is_official_build=true']

  args += [
    'target_cpu="' + machine + '"',
    'skia_use_system_expat=false',
    'skia_use_system_libjpeg_turbo=false',
    'skia_use_system_libpng=false',
    'skia_use_system_libwebp=false',
    'skia_use_system_zlib=false',
    'skia_use_sfntly=false',
    'skia_use_freetype=true',
    'skia_use_system_freetype2=false',
    # 'skia_use_harfbuzz=true',
    'skia_use_system_harfbuzz=false',
    'skia_pdf_subset_harfbuzz=true',
    # 'skia_use_icu=true',
    'skia_use_system_icu=false',
    # 'skia_enable_skshaper=true',
    # 'skia_enable_svg=true',
    'skia_enable_skottie=true'
  ]

  if 'macos' == target or isIos:
    args += [
      # 'skia_enable_gpu=true',
      # 'skia_use_gl=true',
      'skia_use_metal=true',
      'extra_cflags_cc=["-frtti"]'
    ]
    if isIos:
      args += ['target_os="ios"']
      if isIosSim:
        args += ['ios_use_simulator=true']
    else:
      if 'arm64' == machine:
        args += ['extra_cflags=["-stdlib=libc++"]']
      else:
        args += ['extra_cflags=["-stdlib=libc++", "-mmacosx-version-min=10.13"]']
  elif 'linux' == target:
    if 'arm64' == machine:
        # TODO: use clang on all targets!
        args += [
            'skia_gl_standard="gles"',
            'extra_cflags_cc=["-fno-exceptions", "-fno-rtti", "-flax-vector-conversions=all", "-D_GLIBCXX_USE_CXX11_ABI=0"]',
            'cc="clang"',
            'cxx="clang++"',
        ]
    else:
        args += [
            'extra_cflags_cc=["-fno-exceptions", "-fno-rtti","-D_GLIBCXX_USE_CXX11_ABI=0"]',
            'cc="gcc-9"',
            'cxx="g++-9"',
        ]
  elif is_win:
    if is_mingw:
      args += [
        'extra_cflags_cc=["-fno-exceptions", "-fno-rtti","-D_GLIBCXX_USE_CXX11_ABI=0", "-fpermissive"]',
        'cc="gcc"',
        'cxx="g++"',
      ]
    else:
      args += [
        # 'skia_use_angle=true',
        'skia_use_direct3d=true',
        'extra_cflags=["-DSK_FONT_HOST_USE_SYSTEM_SETTINGS"]'
      ]
  elif 'android' == target:
    args += [
      'ndk="'+ ndk + '"'
    ]
  elif 'wasm' == target:
    # brew install emscripten binaryen llvm nodejs
    # echo "BINARYEN_ROOT = '/usr/local'" >> ~/.emscripten
    # echo "LLVM_ROOT = '/opt/homebrew/opt/llvm/bin'" >> ~/.emscripten
    # echo "NODE_JS = '/opt/homebrew/bin/node'" >> ~/.emscripten

    # see skia/modules/canvaskit/compile.sh for reference:
    args += [
        'skia_use_dng_sdk=false',
        'skia_use_libjpeg_turbo_decode=true',
        'skia_use_libjpeg_turbo_encode=true',
        'skia_use_libpng_decode=true',
        'skia_use_libpng_encode=true',
        'skia_use_libwebp_decode=true',
        'skia_use_libwebp_encode=true',
        'skia_use_wuffs=true',
        'skia_use_lua=false',
        'skia_use_webgl=true',
        'skia_use_piex=false',
        'skia_use_system_libpng=false',
        'skia_use_system_freetype2=false',
        'skia_use_system_libjpeg_turbo=false',
        'skia_use_system_libwebp=false',
        'skia_enable_tools=false',
        'skia_enable_fontmgr_custom_directory=false',
        'skia_enable_fontmgr_custom_embedded=true',
        'skia_enable_fontmgr_custom_empty=false',
        'skia_use_webgl=true',
        'skia_gl_standard="webgl"',
        'skia_use_gl=true',
        'skia_enable_gpu=true',
        'skia_enable_svg=true', # other targets have this set in skia.gni
        'skia_use_expat=true',   # other targets have this set in skia.gni
        'extra_cflags=["-DSK_SUPPORT_GPU=1", "-DSK_GL", "-DSK_DISABLE_LEGACY_SHADERCONTEXT"]'
    ]

  if 'linux' == host and 'arm64' == host_machine:
    tools_dir = 'tools'
    ninja = 'ninja-linux-arm64'

  ninja_path = os.path.join('..', tools_dir, ninja)

  env = os.environ.copy()

  if is_mingw:
    os.chdir("gn")
    subprocess.check_call(["python", "build/gen.py", "--out-path=out/" + machine, "--platform=mingw"], env=env)
    subprocess.check_call([ninja_path, "-C", "out/" + machine], env=env)
    os.chdir("..")

  os.chdir('skia')

  out = os.path.join('out', build_type + '-' + target + '-' + machine)

  gn = 'gn.exe' if is_win else 'gn'
  if is_mingw:
    gn_path = os.path.join('..', 'gn', 'out', machine, gn)
  else:
    gn_path = os.path.join('bin', gn)

  print([gn_path, 'gen', out, '--args=' + ' '.join(args)])
  subprocess.check_call([gn_path, 'gen', out, '--args=' + ' '.join(args)], env=env)
  subprocess.check_call([ninja_path, '-C', out, 'skia', 'modules'], env=env)

  return 0

if __name__ == '__main__':
  sys.exit(main())
