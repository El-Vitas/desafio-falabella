import { Component, type ReactNode } from "react";

import { Messages } from "../constants/messages";
import { ErrorState } from "./ErrorState";

interface IProps {
  children: ReactNode;
}

interface IState {
  hasFailed: boolean;
}

export class RenderErrorBoundary extends Component<IProps, IState> {
  state: IState = { hasFailed: false };

  static getDerivedStateFromError(): IState {
    return { hasFailed: true };
  }

  render(): ReactNode {
    if (this.state.hasFailed) {
      return (
        <ErrorState
          message={Messages.renderFailed}
          onRetry={() => this.setState({ hasFailed: false })}
        />
      );
    }
    return this.props.children;
  }
}
