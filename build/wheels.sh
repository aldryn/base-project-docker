while read package; do
  pip wheel --wheel-dir=/wheels/ $package
done < /build/wheels.txt