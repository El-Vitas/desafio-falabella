export const sortDescending = <TItem,>(
  items: readonly TItem[],
  valueOf: (item: TItem) => number | null,
): TItem[] =>
  [...items].sort(
    (first, second) =>
      (valueOf(second) ?? Number.NEGATIVE_INFINITY) - (valueOf(first) ?? Number.NEGATIVE_INFINITY),
  );

export const shareOfMaximum = (value: number | null, maximum: number): number =>
  value === null || maximum <= 0 ? 0 : value / maximum;

export const positiveMaximum = <TItem,>(
  items: readonly TItem[],
  valueOf: (item: TItem) => number | null,
): number => Math.max(0, ...items.map((item) => valueOf(item) ?? 0));

export const isLeadingValue = (value: number | null, maximum: number): boolean =>
  maximum > 0 && value === maximum;

export const leadersOf = <TItem,>(
  items: readonly TItem[],
  valueOf: (item: TItem) => number | null,
): TItem[] => {
  const maximum = positiveMaximum(items, valueOf);
  return items.filter((item) => isLeadingValue(valueOf(item), maximum));
};

export const tieSuffix = (leaderCount: number): string =>
  leaderCount > 1 ? ` · tied with ${leaderCount - 1} more` : "";
