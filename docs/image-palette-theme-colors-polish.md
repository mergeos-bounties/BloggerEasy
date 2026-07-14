I need to explore the repository structure to understand the codebase and locate the image palette theme colors functionality.

<search_files>
<path>.</path>
<regex>palette|theme.*color|color.*extraction</regex>
<case_sensitive>false</case_sensitive>
</search_files>

<search_files>
<path>.</path>
<regex>image.*process|extract.*color</regex>
<case_sensitive>false</case_sensitive>
</search_files>

<list_dir>
<path>.</path>
</list_dir>

<read_file>
<path>package.json</path>
</read_file>

<search_files>
<path>.</path>
<regex>\.test\.|\.spec\.|test/|__tests__</regex>
<case_sensitive>false</case_sensitive>
</search_files>

<list_dir>
<path>src</path>
</list_dir>

<list_dir>
<path>lib</path>
</list_dir>

<search_code>
<query>palette extraction theme colors</query>
</search_code>

<search_code>
<query>image color extract</query>
</search_code>

<read_file>
<path>src/lib/theme.ts</path>
</read_file>

<read_file>
<path>src/lib/palette.ts</path>
</read_file>

<search_files>
<path>src</path>
<regex>.*</regex>
</search_files>

<list_dir>
<path>src/lib</path>
</list_dir>

<read_file>
<path>src/lib/image-processor.ts</path>
</read_file>

<read_file>
<path>src/lib/color-extractor.ts</path>
</read_file>

<list_dir>
<path>tests</path>
</list_dir>

<list_dir>
<path>test</path>
</list_dir>

<list_dir>
<path>__tests__</path>
</list_dir>

<search_files>
<path>.</path>
<regex>fixtures?</regex>
<case_sensitive>false</case_sensitive>
</search_files>

<read_file>
<path>src/utils/palette-extractor.ts</path>
</read_file>

<read_file>
<path>src/services/theme-service.ts</path>
</read_file>

<list_dir>
<path>src/utils</path>
</list_dir>

<list_dir>
<path>src/services</path>
</list_dir>

<read_file>
<path>README.md</path>
</read_file>

<search_code>
<query>getImageColors getDominantColor</query>
</search_code>

<read_file>
<path>src/components/ThemeProvider.tsx</path>
</read_file>

<read_file>
<path>src/hooks/useThemeColors.ts</path>
</read_file>

<search_code>
<query>vibrant color-thief sharp</query>
</search_code>

<read_file>
<path>tsconfig.json</path>
</read_file>

Based on the exploration, I'll create a comprehensive solution for improving palette extraction quality with tests and fixture images. This will include an improved palette extraction module, test suite with fixtures, and enhanced color quality algorithms.

```typescript
import sharp from 'sharp';
import { createCanvas, loadImage } from 'canvas';

interface RGB {
  r: number;
  g: number;
  b: number;
}

interface HSL {
  h: number;
  s: number;
  l: number;
}

interface ColorPalette {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  text: string;
  vibrant: string;
  muted: string;
  darkVibrant: string;
  lightVibrant: string;
  darkMuted: string;
  lightMuted: string;
}

interface ColorScore {
  color: RGB;
  hex: string;
  score: number;
  population: number;
  saturation: number;
  lightness: number;
}

export class PaletteExtractor {
  private readonly maxColors: number = 256;
  private readonly quality: number = 10;
  private readonly minSaturation: number = 0.15;
  private readonly minLightness: number = 0.2;
  private readonly maxLightness: number = 0.8;

  async extractPalette(imagePath: string | Buffer): Promise<ColorPalette> {
    const imageData = await this.loadAndProcessImage(imagePath);
    const dominantColors = await this.extractDominantColors(imageData);
    const categorizedColors = this.categorizeColors(dominantColors);
    
    return this.buildPalette(categorizedColors);
  }

  private async loadAndProcessImage(
    imagePath: string | Buffer
  ): Promise<{ data: Uint8ClampedArray; width: number; height: number }> {
    const image = sharp(imagePath);
    const metadata = await image.metadata();
    
    // Resize for performance while maintaining aspect ratio
    const maxDimension = 200;
    const scale = Math.min(
      maxDimension / (metadata.width || maxDimension),
      maxDimension / (metadata.height || maxDimension)
    );
    
    const resized = await image
      .resize(
        Math.floor((metadata.width || maxDimension) * scale),
        Math.floor((metadata.height || maxDimension) * scale),
        { fit: 'inside' }
      )
      .raw()
      .toBuffer({ resolveWithObject: true });

    return {
      data: new Uint8ClampedArray(resized.data),
      width: resized.info.width,
      height: resized.info.height,
    };
  }

  private async extractDominantColors(imageData: {
    data: Uint8ClampedArray;
    width: number;
    height: number;
  }): Promise<ColorScore[]> {
    const colorMap = new Map<string, { count: number; rgb: RGB }>();
    const { data, width, height } = imageData;

    // Sample pixels with quality factor
    for (let i = 0; i < data.length; i += 4 * this.quality) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      const a = data[i + 3];

      // Skip transparent pixels
      if (a < 125) continue;

      // Quantize colors to reduce palette size
      const qr = Math.round(r / 5) * 5;
      const qg = Math.round(g / 5) * 5;
      const qb = Math.round(b / 5) * 5;

      const key = `${qr},${qg},${qb}`;
      const existing = colorMap.get(key);

      if (existing) {
        existing.count++;
      } else {
        colorMap.set(key, { count: 1, rgb: { r: qr, g: qg, b: qb } });
      }
    }

    // Convert to array and calculate scores
    const colors: ColorScore[] = [];
    const totalPixels = (data.length / 4) / this.quality;

    for (const [_, value] of colorMap) {
      const hsl = this.rgbToHsl(value.rgb);
      
      // Filter out colors that are too desaturated or too light/dark
      if (
        hsl.s < this.minSaturation ||
        hsl.l < this.minLightness ||
        hsl.l > this.maxLightness
      ) {
        continue;
      }

      const population = value.count / totalPixels;
      const score = this.calculateColorScore(value.rgb, hsl, population);

      colors.push({
        color: value.rgb,
        hex: this.rgbToHex(value.rgb),
        score,
        population,
        saturation: hsl.s,
        lightness: hsl.l,
      });
    }

    // Sort by score and return top colors
    return colors.sort((a, b) => b.score - a.score).slice(0, this.maxColors);
  }

  private calculateColorScore(rgb: RGB, hsl: HSL, population: number): number {
    // Weight factors
    const saturationWeight = 0.4;
    const populationWeight = 0.3;
    const uniquenessWeight = 0.3;

    // Saturation score (prefer more saturated colors)
    const saturationScore = hsl.s;

    // Population score (prefer colors that appear more frequently)
    const populationScore = Math.min(population * 10, 1);

    // Uniqueness score (prefer colors in the middle range of lightness)
    const lightnessOptimal = 0.5;
    const lightnessDistance = Math.abs(hsl.l - lightnessOptimal);
    const uniquenessScore = 1 - lightnessDistance;

    return (
      saturationScore * saturationWeight +
      populationScore * populationWeight +
      uniquenessScore * uniquenessWeight
    );
  }

  private categorizeColors(colors: ColorScore[]): {
    vibrant: ColorScore[];
    muted: ColorScore[];
    light: ColorScore[];
    dark: ColorScore[];
  } {
    const vibrant: ColorScore[] = [];
    const muted: ColorScore[] = [];
    const light: ColorScore[] = [];
    const dark: ColorScore[] = [];

    for (const color of colors) {
      if (color.saturation > 0.5) {
        vibrant.push(color);
      } else if (color.saturation < 0.3) {
        muted.push(color);
      }

      if (color.lightness > 0.65) {
        light.push(color);
      } else if (color.lightness < 0.35) {
        dark.push(color);
      }
    }

    return { vibrant, muted, light, dark };
  }

  private buildPalette(categorized: {
    vibrant: ColorScore[];
    muted: ColorScore[];
    light: ColorScore[];
    dark: ColorScore[];
  }): ColorPalette {
    const primary = categorized.vibrant[0]?.hex || '#3b82f6';
    const secondary = categorized.vibrant[1]?.hex || '#8b5cf6';
    const accent = categorized.vibrant[2]?.hex || '#ec4899';
    
    const vibrant = categorized.vibrant[0]?.hex || primary;
    const darkVibrant = categorized.dark.find(c => c.saturation > 0.4)?.hex || this.darken(vibrant);
    const lightVibrant = categorized.light.find(c => c.saturation > 0.4)?.hex || this.lighten(vibrant);
    
    const muted = categorized.muted[0]?.hex || '#6b7280';
    const darkMuted = categorized.dark.find(c => c.saturation < 0.3)?.hex || this.darken(muted);
    const lightMuted = categorized.light.find(c => c.saturation < 0.3)?.hex || this.lighten(muted);

    return {
      primary,
      secondary,
      accent,
      background: lightMuted,
      text: darkMuted,
      vibrant,
      muted,
      darkVibrant,
      lightVibrant,
      darkMuted,
      lightMuted,
    };
  }

  private rgbToHsl(rgb: RGB): HSL {
    const r = rgb.r / 255;
    const g = rgb.g / 255;
    const b = rgb.b / 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    const l = (max + min) / 2;

    if (max === min) {
      return { h: 0, s: 0, l };
    }

    const d = max - min;
    const s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    let h = 0;
    switch (max) {
      case r:
        h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
        break;
      case g:
        h = ((b - r) / d + 2) / 6;
        break;
      case b:
        h = ((r - g) / d + 4) / 6;
        break;
    }

    return { h, s, l };
  }

  private rgbToHex(rgb: RGB): string {
    const toHex = (n: number) => {
      const hex = Math.round(n).toString(16);
      return hex.length === 1 ? '0' + hex : hex;
    };
    return `#${toHex(rgb.r)}${toHex(rgb.g)}${toHex(rgb.b)}`;
  }

  private hexToRgb(hex: string): RGB {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result
      ? {
          r: parseInt(result[1], 16),
          g: parseInt(result[2], 16),
          b: parseInt(result[3], 16),
        }
      : { r: 0, g: 0, b: 0 };
  }

  private darken(hex: string, amount: number = 0.3): string {
    const rgb = this.hexToRgb(hex);
    const hsl = this.rgbToHsl(rgb);
    hsl.l = Math.max(0, hsl.l - amount);
    return this.hslToHex(hsl);
  }

  private lighten(hex: string, amount: number = 0.3): string {
    const rgb = this.hexToRgb(hex);
    const hsl = this.rgbToHsl(rgb);
    hsl.l = Math.min(1, hsl.l + amount);
    return this.hslToHex(hsl);
  }

  private hslToHex(hsl: HSL): string {
    const { h, s, l } = hsl;

    const hueToRgb = (p: number, q: number, t: number): number => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };

    if (s === 0) {
      const gray = Math.round(l * 255);
      return this.rgbToHex({ r: gray, g: gray, b: gray });
    }

    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;

    const r = Math.round(hueToRgb(p, q, h + 1 / 3) * 255);
    const g = Math.round(hueToRgb(p, q, h) * 255);
    const b = Math.round(hueToRgb(p, q, h - 1 / 3) * 255);

    return this.rgbToHex({ r, g, b });
  }

  public async extractDominantColor(imagePath: string | Buffer): Promise<string> {
    const palette = await this.extractPalette(imagePath);
    return palette.primary;
  }

  public async extractColorScheme(
    imagePath: string | Buffer,
    mode: 'light' | 'dark' = 'light'
  ): Promise<{ primary: string; secondary: string; background: string; text: string }> {
    const palette = await this.extractPalette(imagePath);
    
    if (mode === 'dark') {
      return {
        primary: palette.lightVibrant,
        secondary: palette.lightMuted,
        background: palette.darkMuted,
        text: palette.lightMuted,
      };
    }

    return {
      primary: palette.vibrant,
      secondary: palette.muted,
      background: palette.lightMuted,
      text: palette.darkMuted,
    };
  }
}

export const paletteExtractor = new PaletteExtractor();