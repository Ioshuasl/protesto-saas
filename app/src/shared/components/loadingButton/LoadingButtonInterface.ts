import { Button } from '@/components/ui/button';

export default interface LoadingButtonInterface extends React.ComponentProps<typeof Button> {
  text: string;
  textLoading: string;
  loading?: boolean;
}
