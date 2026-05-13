import en from './en.json';
import zh from './zh.json';

export const translations = { en, zh } as const;
export type Locale = keyof typeof translations;

export function getLocale(url: URL): Locale {
  const lang = url.pathname.split('/')[1];
  return lang === 'zh' ? 'zh' : 'en';
}

export function t(locale: Locale, key: string): string {
  const keys = key.split('.');
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let value: any = translations[locale];
  for (const k of keys) {
    value = value?.[k];
  }
  return value ?? key;
}

export function getLocalePath(locale: Locale, path: string): string {
  if (path.startsWith('/')) {
    path = path.slice(1);
  }
  if (locale === 'en') {
    return `/en/${path}`;
  }
  return `/zh/${path}`;
}
