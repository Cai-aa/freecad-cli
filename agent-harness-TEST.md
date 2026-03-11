# TEST.md

## Plan
- verify `fc doctor`
- verify `fc doc create`
- verify `fc create box`
- verify `fc create cylinder`
- verify `fc doc objects`

## Results
- `fc doc create harness_demo` ✅
- `fc create box harness_demo box1 --length 20 --width 10 --height 5` ✅
- `fc create cylinder harness_demo cyl1 --radius 4 --height 12 --x 25` ✅
- `fc doc objects harness_demo` ✅
