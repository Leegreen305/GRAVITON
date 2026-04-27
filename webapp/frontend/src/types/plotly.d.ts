declare module "react-plotly.js" {
    import { Component } from "react";

    interface PlotParams {
        data: Array<Record<string, unknown>>;
        layout?: Record<string, unknown>;
        config?: Record<string, unknown>;
        style?: React.CSSProperties;
        className?: string;
        useResizeHandler?: boolean;
        onInitialized?: (figure: Record<string, unknown>, graphDiv: HTMLElement) => void;
        onUpdate?: (figure: Record<string, unknown>, graphDiv: HTMLElement) => void;
        onSelected?: (event: Record<string, unknown>) => void;
        onClick?: (event: Record<string, unknown>) => void;
        onHover?: (event: Record<string, unknown>) => void;
        onRelayout?: (event: Record<string, unknown>) => void;
    }

    class Plot extends Component<PlotParams> { }

    export default Plot;
}
