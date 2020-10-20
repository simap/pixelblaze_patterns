export function beforeRender(delta) {
  t1 = time(.1)
}

export function render(index) {
  h = t1 + index/pixelCount
  s = 1
  v = 1
  hsv(h, s, v)
}