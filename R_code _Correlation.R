data(EWDI_data)
head(EWDI_data)
dim(EWDI_data)
attach(EWDI_data)
cor.test(`FET`,`Crop yield`)
x <- `FET`
y <- `Crop yield`
# Plot with main and axis titles
# Change point shape (pch = 19) and remove frame.
# Add regression line
plot(x, y, main = "FET vs Crop yield",
     xlab = "FET", ylab = "Crop yield",
     pch = 19, frame = TRUE)
abline(lm(y ~ x, data = mtcars), col = "blue")

parameter <- c(rep('Precipitation',13),rep('SPEI-10',13),rep('PET',13)
               ,rep('Temp',13),rep('Crop yield',13),rep('Nitrogen Fertilization',13)
               ,rep('Crop yield',13))
weight <- c(Precipitation, `SPEI-10`,PET,Temp,Crop yield,`Nitrogen Fertilization`,`Crop yield`)
df <- data.frame (parameter, weight)
Farm.aov <- aov(weight ~ parameter, data = df)
summary(Farm.aov)
