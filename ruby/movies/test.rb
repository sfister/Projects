movies = { "terminator".to_sym =>  3,
"hitch".to_sym => 3}

puts "what to do: add, update, display, delete"

choice = gets.chomp

case choice.downcase()

when "add"
    puts "what is the movie title?"
    title = gets.chomp
    if movies[title.to_sym] == nil
        puts "What is the rating of the movie"
        rating = gets.chomp
        movies[title.to_sym]=rating.to_i
    else
        puts "Movies: #{title} already exists."
    end
when "update"
    puts "What Movie title would you like to update?"
    title = gets.chomp
    if movies[title.to_sym] == nil
        puts "Movie #{title} not found."
    else
        puts "What is the new rating for #{title}?"
        rating = gets.chomp
        movies[title.to_sym] = rating.to_i
    end
when "display"
    movies.each do |movie, rating|puts "#{movie}: #{rating}" end
when "delete"
    puts "Movie to delete?"
    title = gets.chomp
    if movies[title.to_sym] == nil
        puts "#{title} not found to delete."
    else
        movies.delete(title.to_sym)
    end
else
    puts "Error!"
end

puts movies

