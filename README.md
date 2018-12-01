# Face tracking driver
This software lets you control an external device by using facetracking.

It's especially useful for webcam tracking, but it can be used for any other pointed device.

## How it works
The **GenericOutput** should be enough for most cases, it prints out the displacement vector relative to the
pivot point.

The **displacement vector** is a normalized vector that always points to the pivots point position.

Algorithm:
  - tracked face relative distance > threshold: Prints out displacement vector until the relative distance <=
    rest threshold
  - tracked face relative distance <= threshold: Clamps the vector to (0, 0)
