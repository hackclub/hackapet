# Colosion
A 128x128 game about subtractive color mixing.

## Guide
Your goal is to color-match the enemy tiles and shoot them before they reach you. 

You can use any combination of <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/>, <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/>, and <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/>— but you're only given three portions of color to work with, so make do with what you have!

**NOTE:** This is a simplification of subtractive color mixing! This game is only aimed to give a fundamental idea of how it works.

<details>
    <summary>Color Combination Guide</summary>
    <!-- red: MY -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> + 
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> = 
    <img valign='middle' alt='red' src='https://readme-swatches.vercel.app/FF6060?style=round'/>
    </div>
    <!-- orange: MYY -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> + 
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> + 
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> = 
    <img valign='middle' alt='orange' src='https://readme-swatches.vercel.app/F69F5A?style=round'/>
    </div>
    <!-- scarlet: MMY -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> + 
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> + 
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> =
    <img valign='middle' alt='scarlet' src='https://readme-swatches.vercel.app/FE7196?style=round'/>
    </div>
    <!-- green: CY -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> = 
    <img valign='middle' alt='green' src='https://readme-swatches.vercel.app/50D57E?style=round'/>
    </div>
    <!-- lime: CYY -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> +
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> = 
    <img valign='middle' alt='lime' src='https://readme-swatches.vercel.app/B2EC71?style=round'/>
    </div>
    <!-- blue: CM -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> = 
    <img valign='middle' alt='blue' src='https://readme-swatches.vercel.app/526DEC?style=round'/>
    </div>
    <!-- black: CMY -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> +
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> = 
    <img valign='middle' alt='black' src='https://readme-swatches.vercel.app/393942?style=round'/>
    </div>
    <!-- purple: CMM -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> +
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> =
    <img valign='middle' alt='purple' src='https://readme-swatches.vercel.app/9259DC?style=round'/>
    </div>
    <!-- turquoise: CCY -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='yellow' src='https://readme-swatches.vercel.app/FBE783?style=round'/> = 
    <img valign='middle' alt='turquoise' src='https://readme-swatches.vercel.app/3DD5C1?style=round'/>
    </div>
    <!-- azure: CCM -->
    <div style="margin-bottom: 16px;">
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='cyan' src='https://readme-swatches.vercel.app/83DFFB?style=round'/> +
    <img valign='middle' alt='magenta' src='https://readme-swatches.vercel.app/FB83CF?style=round'/> =
    <img valign='middle' alt='azure' src='https://readme-swatches.vercel.app/57AAF7?style=round'/>
    </div>
</details>

## Controls
### RIGHT ARROW: 
Move to the next button.

### SPACE: 
Toggle the number of portions of your currently selected color.

### RETURN:
* **COLOR MIXING:** Finish mixing your color.
* **ARROW SELECTION:** Shoot!