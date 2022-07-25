#! /usr/bin/env python3

import common, os, subprocess, sys

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir, 'skia'))

  build_type = common.build_type()
  machine = common.machine()
  host = common.host()
  host_machine = common.host_machine()
  target = common.target()
  ndk = common.ndk()

  tools_dir = "depot_tools"
  ninja = 'ninja.exe' if 'windows' == host else 'ninja'

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

  if 'macos' == target or 'ios' == target:
    args += [
      # 'skia_enable_gpu=true',
      # 'skia_use_gl=true',
      'skia_use_metal=true',
      'extra_cflags_cc=["-frtti"]'
    ]
    if 'ios' == target:
      args += ['target_os="ios"']
    elif 'tvos' == target:
      args += ['target_os="tvos"']
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
  elif 'windows' == target:
    args += [
      # 'skia_use_angle=true',
      'skia_use_direct3d=true',
      'extra_cflags=["-DSK_FONT_HOST_USE_SYSTEM_SETTINGS"]',
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
        'cc="emcc"',
        'cxx="emcc"',
        'ar="emar"',
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
        'extra_cflags=["-DSK_SUPPORT_GPU=1", "-DSK_GL", "-DSK_DISABLE_LEGACY_SHADERCONTEXT"]'
    ]

  if 'linux' == host and 'arm64' == host_machine:
    tools_dir = 'tools'
    ninja = 'ninja-linux-arm64'

  out = os.path.join('out', build_type + '-' + target + '-' + machine)
  gn = 'gn.exe' if 'windows' == host else 'gn'
  print([os.path.join('bin', gn), 'gen', out, '--args=' + ' '.join(args)])
  subprocess.check_call([os.path.join('bin', gn), 'gen', out, '--args=' + ' '.join(args)])
  subprocess.check_call([os.path.join('..', tools_dir, ninja), '-C', out, 'skia', 'modules'])

  return 0

if __name__ == '__main__':
  sys.exit(main())
