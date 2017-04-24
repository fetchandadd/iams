# iams
Image analysis microservice

## API

For the following examples [HTTPie](https://httpie.org/) is used to manage HTTP connections.

### Average hash

```bash
http localhost:8080/v1/average_hash < source.jpg
```

```json
{
    "average_hash": "fe7838020078785e"
}
```

### Difference hash

```bash
http localhost:8080/v1/difference_hash < source.jpg
```

```json
{
    "difference_hash": "6f2d0d4b232f2f6b"
}
```

### Perception hash

```bash
http localhost:8080/v1/perception_hash < source.jpg
```

```json
{
    "perception_hash": "212bb9e187f19971"
}
```

### Wavelet hash

```bash
http localhost:8080/v1/wavelet_hash < source.jpg
```

```json
{
    "wavelet_hash": "ff7e780208487c5e"
}
```

### Hashes

```bash
http localhost:8080/v1/hashes < source.jpg
```

```json
{
    "average_hash": "fe7838020078785e",
    "difference_hash": "6f2d0d4b232f2f6b",
    "perception_hash": "212bb9e187f19971",
    "wavelet_hash": "ff7e780208487c5e"
}
```

### Top n colors

```bash
http localhost:8080/v1/colors n==3 < source.jpg
```

```
[
    {
        "color": {
            "b": 47,
            "g": 107,
            "hex": "556B2F",
            "name": "Dark Olive Green",
            "r": 85
        },
        "frequency": 0.1875
    },
    {
        "color": {
            "b": 105,
            "g": 105,
            "hex": "696969",
            "name": "Dim Gray",
            "r": 105
        },
        "frequency": 0.1528
    },
    {
        "color": {
            "b": 79,
            "g": 79,
            "hex": "2F4F4F",
            "name": "Dark Slate Gray",
            "r": 47
        },
        "frequency": 0.1389
    }
]
```
