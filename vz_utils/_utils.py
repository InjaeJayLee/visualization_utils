from typing import Any

import matplotlib.pyplot as plt


def draw_broken_histogram(data: Any, *,
                          bottom: float, broken_bottom: float, broken_top: float, top: float, bins: int,
                          color: Any, title: str, x_label: str, y_label: str,
                          title_font_size: int = 14, x_label_font_size: int = 12):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax1.set_ylim(broken_top, top)
    ax2.set_ylim(bottom, broken_bottom)
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False)
    ax2.xaxis.tick_bottom()

    d = .01
    kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
    ax1.plot((-d, +d), (-d, +d), **kwargs)
    ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)
    kwargs.update(transform=ax2.transAxes)
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

    ax1.hist(data, bins=bins, color=color)
    ax2.hist(data, bins=bins, color=color)

    fig.text(0.5, 0.94, title, ha='center', fontdict={'fontsize': title_font_size})
    fig.text(0.02, 0.5, y_label, va='center', rotation='vertical')
    plt.xlabel(x_label, fontsize=x_label_font_size)

    plt.show()


def draw_broken_line_plot(data: pd.DataFrame, 
                          x: str, y: str, hue: str, col: str, 
                          bottom: float | int, broken_bottom: float | int, broken_top: float | int, top: float | int,
                          x_label: str, y_label: str, main_title: str,
                          d: float=0.01,
                          height_ratios: list[int,int]=[1, 1]):
    cols = sorted(data[col].unique())
    n_cols = len(cols)
    
    # Create the figure
    fig, axes = plt.subplots(2, n_cols, sharex=True, 
                             gridspec_kw={'height_ratios': height_ratios},
                             figsize=(n_cols * 5, 6))
    
    # Handle the case where there is only 1 column (axes becomes 1D)
    if n_cols == 1:
        axes = axes.reshape(2, 1)

    for i, col_val in enumerate(cols):
        subset = data[data[col] == col_val]
        ax_top = axes[0, i]
        ax_bot = axes[1, i]
        
        # Plot data on both top and bottom segments
        for val in subset[hue].unique():
            line_data = subset[subset[hue] == val]
            label = f"{val}" # Simplified label for legend
            ax_top.plot(line_data[x], line_data[y], marker='o', label=label)
            ax_bot.plot(line_data[x], line_data[y], marker='o')

        # Set specific Y-limits for the break
        ax_top.set_ylim(broken_top, top)
        ax_bot.set_ylim(bottom, broken_bottom)
        
        # Style the break: Hide unnecessary spines
        ax_top.spines['bottom'].set_visible(False)
        ax_bot.spines['top'].set_visible(False)
        ax_top.tick_params(labelbottom=False, bottom=False)
        
        # --- SCALED BREAK MARKS ---
        # We adjust the Y-extension of the markers based on height ratios
        # to ensure the angle looks consistent across both subplots.
        dy_top = d * (height_ratios[1] / height_ratios[0]) # Scale up for the short axis
        dy_bot = d 

        # Top marks (slanted steeper in coordinate space)
        kw = dict(transform=ax_top.transAxes, color='k', clip_on=False)
        ax_top.plot((-d, +d), (-dy_top, +dy_top), **kw)        
        ax_top.plot((1 - d, 1 + d), (-dy_top, +dy_top), **kw)  
        
        # Bottom marks (standard slant)
        kw.update(transform=ax_bot.transAxes)
        ax_bot.plot((-d, +d), (1 - dy_bot, 1 + dy_bot), **kw)  
        ax_bot.plot((1 - d, 1 + d), (1 - dy_bot, 1 + dy_bot), **kw)
        
        # Set the subtitle for each column
        ax_top.set_title(f"VIP: {col_val}", fontweight='bold')

        # Add legend to the first top subplot
        if i == n_cols - 1:
            ax_top.legend(title=hue, loc='upper right', bbox_to_anchor=(1.3, 1))

    # --- GLOBAL LABELS ---
    fig.suptitle(main_title, fontsize=16, y=1.02)    
    fig.text(0.5, -0.02, x_label, ha='center', fontsize=12)  
    fig.text(-0.02, 0.5, y_label, va='center', rotation='vertical', fontsize=12)

    plt.tight_layout()
    plt.show()
