# ffcompress

ffmpeg-based CLI tool for compressing video files

## Usage
```
ffcompress FILE SIZE [options]
```

| Arg | Description |
| ---- | ----------- |
| `FILE` | The target video file |
| `SIZE` | Target output size, e.g. `1g`, `25mb`, `500KB` |

## Options
| Flag | Action |
| ------ | ------ |
| `-y` | Overwrite output files without asking for confirmation |

## License
ffcompress is distributed under the GNU [GPL-3.0 License](https://github.com/fergusch/ffcompress/blob/main/LICENSE).