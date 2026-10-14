"use client";

import { useId, type ReactNode, type RefObject } from "react";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import { FiChevronLeft, FiChevronRight } from "react-icons/fi";
import type { CarouselAfterChangeState } from "@/hooks/useCarousel";
import useMounted from "@/hooks/useMounted";


export const DEFAULT_CAROUSEL_RESPONSIVE = {
  desktop: { breakpoint: { max: 4000, min: 1024 }, items: 5, slidesToSlide: 5 },
  laptop: { breakpoint: { max: 1023, min: 768 }, items: 4, slidesToSlide: 4 },
  tablet: { breakpoint: { max: 767, min: 640 }, items: 3, slidesToSlide: 3 },
  mobile: { breakpoint: { max: 639, min: 0 }, items: 2, slidesToSlide: 2 },
};

interface CarouselSectionProps<T> {
  title: string;
  items: T[];
  getItemKey: (item: T) => string | number;
  renderItem: (item: T) => ReactNode;
  carouselRef: RefObject<Carousel | null>;
  isLoading: boolean;
  canScrollPrevious: boolean;
  canScrollNext: boolean;
  onScrollPrevious: () => void;
  onScrollNext: () => void;
  onAfterChange: (
    previousSlide: number,
    state: CarouselAfterChangeState,
  ) => void;
  responsive?: typeof DEFAULT_CAROUSEL_RESPONSIVE;
}

export default function CarouselSection<T>({
  title,
  items,
  getItemKey,
  renderItem,
  carouselRef,
  isLoading,
  canScrollPrevious,
  canScrollNext,
  onScrollPrevious,
  onScrollNext,
  onAfterChange,
  responsive = DEFAULT_CAROUSEL_RESPONSIVE,
}: CarouselSectionProps<T>) {
  const titleId = useId();
  const { isMounted } = useMounted();

  return (
    <section aria-labelledby={titleId} className="mx-auto max-w-375">
      <div className="mb-4 flex items-center justify-between border-b border-surface-border pb-2">
        <h1 id={titleId} className="text-2xl font-bold text-foreground">
          {title}
        </h1>

        <div className="flex gap-2">
          <button
            type="button"
            aria-label={`${title}: anteriores`}
            title="Anteriores"
            onClick={onScrollPrevious}
            disabled={!canScrollPrevious && isMounted}
            className="cursor-pointer flex size-9 items-center justify-center rounded-full border border-surface-border text-foreground-muted transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-surface-border disabled:hover:bg-transparent disabled:hover:text-foreground-muted"
          >
            <FiChevronLeft aria-hidden="true" className="size-5" />
          </button>
          <button
            type="button"
            aria-label={`${title}: próximos`}
            title="Próximos"
            onClick={onScrollNext}
            disabled={(!canScrollNext || isLoading) && isMounted}
            className="cursor-pointer flex size-9 items-center justify-center rounded-full border border-surface-border text-foreground-muted transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-surface-border disabled:hover:bg-transparent disabled:hover:text-foreground-muted"
          >
            <FiChevronRight aria-hidden="true" className="size-5" />
          </button>
        </div>
      </div>

      <Carousel
        ref={carouselRef}
        responsive={responsive}
        arrows={false}
        swipeable
        draggable
        infinite={false}
        afterChange={onAfterChange}
        itemClass="flex justify-center px-1.5"
        containerClass="pb-3"
      >
        {items.map((item) => (
          <div key={getItemKey(item)}>{renderItem(item)}</div>
        ))}
      </Carousel>
    </section>
  );
}