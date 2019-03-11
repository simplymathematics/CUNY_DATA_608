df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')
df <- as.data.frame(df)



ui <- fluidPage(
  headerPanel('You Death Rate Changes'),
  sidebarPanel(
    selectInput('disease', 'Disease', unique(df$ICD.Chapter), selected='Certain conditions originating in the perinatal period')
  ),
  mainPanel(
    plotOutput('plot1')
  )
)

server <- shinyServer(function(input, output, session) {
  
  selectedData <- reactive({
    dfSlice <- df %>%
      filter(ICD.Chapter == input$disease)
  })
  
  output$plot1 <- renderPlot({
    
    dfSlice <- df %>%
      filter(ICD.Chapter == input$disease)
    
    ggplot(selectedData(), aes(x = State, y = Crude.Rate)) +
      geom_bar(stat = 'identity')
  })
  
  output$stats <- renderPrint({
    dfSliceTier <- selectedData() %>%
      filter(Tier == input$tier)
    
    summary(dfSliceTier$HPI)
  })
  
})

shinyApp(ui = ui, server = server)