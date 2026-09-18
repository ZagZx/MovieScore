import { useRef, useState } from "react";
import type Carousel from "react-multi-carousel";

export interface CarouselAfterChangeState {
  currentSlide: number;
  slidesToShow: number;
}

export interface LoadMoreResult<T> {
  items: T[];
  hasMore: boolean;
}

interface UseCarouselOptions<T> {
  initialItems: T[];
  getItemId: (item: T) => string | number;
  initialHasMore?: boolean;
  // Busca a próxima "página" de itens. Quem chama decide como identificar
  // qual página/cursor buscar em seguida; o hook só sabe "tem mais?".
  loadMore?: () => Promise<LoadMoreResult<T> | null>;
}

interface UseCarouselResult<T> {
  carouselRef: React.RefObject<Carousel | null>;
  items: T[];
  isLoading: boolean;
  canScrollPrevious: boolean;
  canScrollNext: boolean;
  scrollPrevious: () => void;
  scrollNext: () => void;
  handleAfterChange: (
    previousSlide: number,
    state: CarouselAfterChangeState,
  ) => void;
}

export default function useCarousel<T>({
  initialItems,
  getItemId,
  initialHasMore = false,
  loadMore,
}: UseCarouselOptions<T>): UseCarouselResult<T> {
  const carouselRef = useRef<Carousel>(null);
  const [items, setItems] = useState(initialItems);
  const [hasMore, setHasMore] = useState(initialHasMore);
  const [isLoading, setIsLoading] = useState(false);
  const [canScrollPrevious, setCanScrollPrevious] = useState(false);
  const [canScrollNext, setCanScrollNext] = useState(initialItems.length > 0);

  function appendItems(newItems: T[]) {
    setItems((currentItems) => {
      const currentIds = new Set(currentItems.map(getItemId));
      return [
        ...currentItems,
        ...newItems.filter((item) => !currentIds.has(getItemId(item))),
      ];
    });
  }

  async function loadMoreIfNeeded() {
    if (!loadMore || !hasMore || isLoading) return;

    setCanScrollNext(false);
    setIsLoading(true);
    try {
      const result = await loadMore();

      if (result) {
        appendItems(result.items);
        setHasMore(result.hasMore);
        setCanScrollNext(result.hasMore);
      }
    } finally {
      setIsLoading(false);
    }
  }

  function handleAfterChange(
    _previousSlide: number,
    state: CarouselAfterChangeState,
  ) {
    const { currentSlide, slidesToShow } = state;
    const isAtEnd = currentSlide + slidesToShow >= items.length;

    setCanScrollPrevious(currentSlide > 0);
    setCanScrollNext(!isAtEnd || Boolean(hasMore && loadMore));

    if (isAtEnd) {
      loadMoreIfNeeded();
    }
  }

  function scrollPrevious() {
    carouselRef.current?.previous(0);
  }

  function scrollNext() {
    carouselRef.current?.next(0);
  }

  return {
    carouselRef,
    items,
    isLoading,
    canScrollPrevious,
    canScrollNext,
    scrollPrevious,
    scrollNext,
    handleAfterChange,
  };
}